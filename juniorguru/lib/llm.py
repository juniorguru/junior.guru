import asyncio
from functools import lru_cache
import json
import logging
import os
from datetime import timedelta
from openai import AsyncOpenAI, InternalServerError, RateLimitError
from juniorguru.lib import loggers
from juniorguru.lib.cache import cache
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from juniorguru.lib.mutations import mutates


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


logger = loggers.from_path(__file__)

limit = asyncio.Semaphore(4)


@lru_cache
def get_client() -> AsyncOpenAI:
    logger.debug("Creating OpenAI client")
    return AsyncOpenAI(api_key=OPENAI_API_KEY)


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
async def ask_for_json(system_prompt: str, user_prompt: str) -> dict:
    client = get_client()
    async with limit:
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=dict(type="json_object"),
        )
    choice = completion.choices[0]
    data = json.loads(choice.message.content)
    data["finish_reason"] = choice.finish_reason
    return data
