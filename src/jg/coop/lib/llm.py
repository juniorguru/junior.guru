import logging
import os
from datetime import timedelta
from enum import StrEnum
from functools import lru_cache
from textwrap import dedent
from typing import overload

import tiktoken
from openai import AsyncOpenAI, InternalServerError, RateLimitError
from openai.types.responses import Response
from pydantic import BaseModel, ValidationError
from tenacity import (
    RetryCallState,
    before_sleep_log,
    retry,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from jg.coop.lib import loggers
from jg.coop.lib.async_utils import limit
from jg.coop.lib.cache import cache
from jg.coop.lib.mutations import mutates


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


logger = loggers.from_path(__file__)


class LLMModel(StrEnum):
    simple = "gpt-4o-mini"
    medium = "gpt-4.1-mini"
    advanced = "gpt-4.1"


@lru_cache
def get_client() -> AsyncOpenAI:
    logger.debug("Creating OpenAI client")
    return AsyncOpenAI(api_key=OPENAI_API_KEY)


@overload
async def ask_llm(
    system_prompt: str,
    user_prompt: str,
    model: LLMModel = LLMModel.simple,
    schema: None = None,
) -> str: ...


@overload
async def ask_llm[Schema: BaseModel](
    system_prompt: str,
    user_prompt: str,
    model: LLMModel = LLMModel.simple,
    schema: type[Schema] = ...,
) -> Schema: ...


VALIDATION_ATTEMPTS = 3


class LLMResponseError(Exception):
    pass


def is_requests_rate_limit_error(exception: RateLimitError) -> bool:
    return exception.type == "requests" and "requests per day" not in exception.message


def is_tokens_rate_limit_error(exception: RateLimitError) -> bool:
    return exception.type == "tokens"


def log_and_reraise_validation_error(retry_state: RetryCallState) -> None:
    # Runs only after the last validation attempt, so the terminal diagnostic
    # is logged at error level before the exception propagates.
    exception = retry_state.outcome.exception()
    logger.error(str(exception))
    raise exception


retry_defaults = {
    "reraise": True,
    "before_sleep": before_sleep_log(logger, logging.DEBUG),
    "stop": stop_after_attempt(5),
}


@mutates("openai", raises=True)
@retry(
    retry=(
        retry_if_exception_type(RateLimitError)
        & retry_if_exception(is_requests_rate_limit_error)
    ),
    wait=wait_random_exponential(min=1, max=60),
    **retry_defaults,
)
@retry(
    retry=(
        retry_if_exception_type(RateLimitError)
        & retry_if_exception(is_tokens_rate_limit_error)
    ),
    wait=wait_random_exponential(min=60, max=5 * 60),
    **retry_defaults,
)
@retry(
    retry=retry_if_exception_type(InternalServerError),
    wait=wait_random_exponential(min=60, max=5 * 60),
    **retry_defaults,
)
@retry(
    retry=retry_if_exception_type(LLMResponseError),
    stop=stop_after_attempt(VALIDATION_ATTEMPTS),
    # Warn before each further attempt; error on the final one (see callback).
    before_sleep=before_sleep_log(logger, logging.WARNING),
    retry_error_callback=log_and_reraise_validation_error,
)
@cache(expire=timedelta(days=60), tag="llm")
async def ask_llm[Schema: BaseModel](
    system_prompt: str,
    user_prompt: str,
    model: LLMModel = LLMModel.simple,
    schema: type[Schema] | None = None,
) -> Schema | str:
    client = get_client()
    async with limit(4):
        logger.debug(
            f"Prompt lengths: {count_tokens(system_prompt)}"
            f" + {count_tokens(user_prompt)} tokens"
        )
        llm_input = [
            {"role": "developer", "content": prompt(system_prompt)},
            {"role": "user", "content": prompt(user_prompt)},
        ]
        if schema:
            # Go through with_raw_response so that, when the SDK fails to parse
            # the structured output, we still have the raw response to inspect
            # (status, refusal, incomplete_details) instead of just an opaque
            # "invalid JSON: EOF" error. The happy path still uses the SDK's own
            # parsing (raw_response.parse()), so we don't reimplement it.
            raw_response = await client.responses.with_raw_response.parse(
                model=str(model), input=llm_input, text_format=schema
            )
            try:
                return raw_response.parse().output_parsed
            except ValidationError as e:
                # Best-effort diagnostic, carried on the exception so the retry
                # decorator can log it; never mask the real error.
                try:
                    reason = describe_raw_response(raw_response.text)
                except Exception as diagnostic_error:
                    reason = f"could not describe response: {diagnostic_error}"
                raise LLMResponseError(
                    f"LLM response failed schema validation: {reason}"
                ) from e
        return (
            await client.responses.create(model=str(model), input=llm_input)
        ).output_text


def describe_response(response: Response) -> str:
    parts = [f"status={response.status!r}"]
    if response.incomplete_details:
        parts.append(f"incomplete_reason={response.incomplete_details.reason!r}")
    if response.error:
        parts.append(f"error={response.error.code!r}: {response.error.message!r}")
    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if content.type == "refusal":
                    parts.append(f"refusal={content.refusal!r}")
    text = response.output_text
    parts.append(f"output_text={text[:500]!r} ({len(text)} chars)")
    return ", ".join(parts)


def describe_raw_response(raw_response_text: str) -> str:
    return describe_response(Response.model_validate_json(raw_response_text))


def count_tokens(text: str) -> int:
    # https://github.com/openai/tiktoken/issues/395#issuecomment-2835806009
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = encoding.encode(text)
    return len(tokens)


def prompt(text: str) -> str:
    return dedent(text).strip()
