import asyncio
from collections.abc import Awaitable, Callable
from functools import partial, wraps


semaphores = {}


def limit(value: int) -> asyncio.Semaphore:
    key = f"{id(asyncio.get_event_loop())}-{value}"
    semaphores.setdefault(key, asyncio.Semaphore(value))
    return semaphores[key]


async def call_async(fn: Callable, *args, **kwargs):
    loop = asyncio.get_running_loop()
    fn_with_args_applied = partial(fn, *args, **kwargs)
    return await loop.run_in_executor(None, fn_with_args_applied)


def make_async(fn: Callable) -> Callable[..., Awaitable]:
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        return await call_async(fn, *args, **kwargs)

    return wrapper
