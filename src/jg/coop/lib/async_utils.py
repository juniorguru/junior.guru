import asyncio
from functools import partial, wraps
from typing import Awaitable, Callable


async def call_async(fn: Callable, *args, **kwargs):
    loop = asyncio.get_running_loop()
    fn_with_args_applied = partial(fn, *args, **kwargs)
    return await loop.run_in_executor(None, fn_with_args_applied)


def make_async(fn: Callable) -> Callable[..., Awaitable]:
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        return await call_async(fn, *args, **kwargs)

    return wrapper
