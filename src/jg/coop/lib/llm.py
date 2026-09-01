import logging
import os
from datetime import timedelta
from enum import StrEnum
from functools import lru_cache
from textwrap import dedent
from typing import overload

import tiktoken
from openai import AsyncOpenAI, InternalServerError, RateLimitError
from pydantic import BaseModel, ValidationError
from tenacity import (
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


class EmptyLLMResponseError(Exception):
    """The LLM returned an empty response, a transient issue worth retrying."""


def is_empty_response_error(error: ValidationError) -> bool:
    """Whether a schema validation failure is caused by an empty LLM response.

    Distinguishes an empty (or whitespace-only) completion, which is a transient
    condition worth retrying, from a genuine schema mismatch or truncated JSON.
    """
    return any(
        detail["type"] == "json_invalid"
        and isinstance(detail.get("input"), str)
        and not detail["input"].strip()
        for detail in error.errors()
    )


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
    validation_attempts: int = 3,
) -> str: ...


@overload
async def ask_llm[Schema: BaseModel](
    system_prompt: str,
    user_prompt: str,
    model: LLMModel = LLMModel.simple,
    schema: type[Schema] = ...,
    validation_attempts: int = 3,
) -> Schema: ...


retry_defaults = {
    "reraise": True,
    "before_sleep": before_sleep_log(logger, logging.DEBUG),
    "stop": stop_after_attempt(5),
}


@mutates("openai", raises=True)
@retry(
    retry=(
        retry_if_exception_type(RateLimitError)
        & retry_if_exception(
            lambda exception: (
                exception.type == "requests"
                and "requests per day" not in exception.message
            )
        )
    ),
    wait=wait_random_exponential(min=1, max=60),
    **retry_defaults,
)
@retry(
    retry=(
        retry_if_exception_type(RateLimitError)
        & retry_if_exception(lambda exception: exception.type == "tokens")
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
    retry=retry_if_exception_type(EmptyLLMResponseError),
    wait=wait_random_exponential(min=2, max=30),
    **retry_defaults,
)
@cache(expire=timedelta(days=60), tag="llm")
async def ask_llm[Schema: BaseModel](
    system_prompt: str,
    user_prompt: str,
    model: LLMModel = LLMModel.simple,
    schema: type[Schema] | None = None,
    validation_attempts: int = 3,
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
            for attempt in range(1, validation_attempts + 1):
                logger.debug(f"Asking LLM with schema validation, attempt #{attempt}")
                try:
                    result = (
                        await client.responses.parse(
                            model=str(model),
                            input=llm_input,
                            text_format=schema,
                            # prompt_cache_retention="24h",
                        )
                    ).output_parsed
                    break
                except ValidationError as e:
                    if is_empty_response_error(e):
                        raise EmptyLLMResponseError(
                            "LLM returned an empty response"
                        ) from e
                    if attempt == validation_attempts:
                        raise
                    logger.warning(f"Schema validation failed, attempt #{attempt}: {e}")
        else:
            result = (
                await client.responses.create(
                    model=str(model),
                    input=llm_input,
                    # prompt_cache_retention="24h",
                )
            ).output_text
            if not result.strip():
                raise EmptyLLMResponseError("LLM returned an empty response")
    return result


def count_tokens(text: str) -> int:
    # https://github.com/openai/tiktoken/issues/395#issuecomment-2835806009
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = encoding.encode(text)
    return len(tokens)


def prompt(text: str) -> str:
    return dedent(text).strip()
