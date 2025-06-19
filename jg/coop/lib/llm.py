import asyncio
import logging
import os
from datetime import timedelta
from enum import StrEnum
from functools import lru_cache
from textwrap import dedent
from typing import TypeVar, overload

import tiktoken
from openai import AsyncOpenAI, InternalServerError, RateLimitError
from pydantic import BaseModel
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from jg.coop.lib import loggers
from jg.coop.lib.cache import cache
from jg.coop.lib.mutations import mutates


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


logger = loggers.from_path(__file__)

limit = asyncio.Semaphore(4)


Schema = TypeVar("T", bound=BaseModel)


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
async def ask_llm(
    system_prompt: str,
    user_prompt: str,
    model: LLMModel = LLMModel.simple,
    schema: type[Schema] = ...,
) -> Schema: ...


retry_defaults = dict(
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.DEBUG),
    stop=stop_after_attempt(5),
)


@mutates("openai", raises=True)
@retry(
    retry=(
        retry_if_exception_type(RateLimitError)
        & retry_if_exception(
            lambda exception: exception.type == "requests"
            and "requests per day" not in exception.message
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
@cache(expire=timedelta(days=60), tag="llm")
async def ask_llm(
    system_prompt: str,
    user_prompt: str,
    model: LLMModel = LLMModel.simple,
    schema: type[Schema] | None = None,
) -> Schema | str:
    client = get_client()
    async with limit:
        logger.debug(
            f"Prompt lengths: {count_tokens(system_prompt)}"
            f" + {count_tokens(user_prompt)} tokens"
        )
        llm_input = [
            {"role": "developer", "content": prompt(system_prompt)},
            {"role": "user", "content": prompt(user_prompt)},
        ]
        if schema:
            result = (
                await client.responses.parse(
                    model=str(model),
                    input=llm_input,
                    text_format=schema,
                )
            ).output_parsed
        else:
            result = (
                await client.responses.create(
                    model=str(model),
                    input=llm_input,
                )
            ).output_text
    return result


def count_tokens(text: str) -> int:
    # https://github.com/openai/tiktoken/issues/395#issuecomment-2835806009
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = encoding.encode(text)
    return len(tokens)


def prompt(text: str) -> str:
    return dedent(text).strip()
