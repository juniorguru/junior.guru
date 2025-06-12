import asyncio
import json
import logging
import os
from datetime import timedelta
from functools import lru_cache
from typing import Literal

import tiktoken
from openai import AsyncOpenAI, InternalServerError, RateLimitError
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


@lru_cache
def get_client() -> AsyncOpenAI:
    logger.debug("Creating OpenAI client")
    return AsyncOpenAI(api_key=OPENAI_API_KEY)


async def ask_for_text(
    system_prompt: str,
    user_prompt: str,
    better_model=False,
) -> str:
    return await _ask_llm(
        system_prompt,
        user_prompt,
        response_format="text",
        better_model=better_model,
    )


async def ask_for_json(
    system_prompt: str,
    user_prompt: str,
    better_model=False,
) -> dict:
    json_text = await _ask_llm(
        system_prompt,
        user_prompt,
        response_format="json_object",
        better_model=better_model,
    )
    return json.loads(json_text)


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
@cache(expire=timedelta(days=60), tag="llm-opinion")
async def _ask_llm(
    system_prompt: str,
    user_prompt: str,
    response_format: Literal["text", "json_object"],
    better_model: bool = False,
) -> dict:
    model = "gpt-4.1-mini" if better_model else "gpt-4o-mini"
    client = get_client()
    async with limit:
        logger.debug(
            f"Prompt lengths: {count_tokens(system_prompt)}"
            f" + {count_tokens(user_prompt)} tokens"
        )
        completion = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": response_format},
        )
    choice = completion.choices[0]
    return choice.message.content


def count_tokens(text: str) -> int:
    # https://github.com/openai/tiktoken/issues/395#issuecomment-2835806009
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = encoding.encode(text)
    return len(tokens)
