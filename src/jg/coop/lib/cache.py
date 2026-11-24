import asyncio
import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import timedelta
from functools import lru_cache, wraps
from typing import Any

from diskcache import Cache
from diskcache.core import ENOVAL, args_to_key, full_name
from jinja2 import BytecodeCache as BaseBytecodeCache
from jinja2.bccache import Bucket

from jg.coop.lib.async_utils import call_async


CACHE_DIR = ".cache"


# avoid circular import, loggers depend on cache
logger = logging.getLogger("jg.coop.lib.cache")

_cache_instances = {}


def get_cache(cache_dir=CACHE_DIR) -> Cache:
    try:
        cache = _cache_instances[cache_dir]
    except KeyError:
        logger.debug(f"Initializing cache: {cache_dir}")
        cache = _cache_instances[cache_dir] = Cache(cache_dir, tag_index=True)
    return cache


def close_cache() -> None:
    if caches := _cache_instances.values():
        logger.debug("Cache clean up")
        for cache in caches:
            try:
                cache.expire()
                cache.close()
            except Exception as e:
                logger.warning(f"Failed to close cache: {e}")


@dataclass
class CachedError:
    exception: Exception


def cache(
    expire: float | timedelta | None = None,
    tag: str | None = None,
    ignore: tuple[int | str] = (),
    errors: tuple[type[Exception], ...] = (),
    errors_expire: float | timedelta | None = None,
) -> Callable:
    """Caches results of the decorated function

    If errors are given, raising one of them is cached as well (for
    errors_expire), so that the next call re-raises it without calling
    the function. Useful for expensive calls which fail repeatedly.
    """
    if isinstance(expire, timedelta):
        expire = expire.total_seconds()
    if isinstance(errors_expire, timedelta):
        errors_expire = errors_expire.total_seconds()

    def decorator(fn: Callable) -> Callable:
        cache = get_cache()

        # Rewriting subset of diskcache.memoize() to support async
        if asyncio.iscoroutinefunction(fn):
            base = (full_name(fn),)

            @wraps(fn)
            async def wrapper(*args, **kwargs) -> Any:
                key = args_to_key(base, args, kwargs, False, ignore)
                result = await call_async(cache.get, key, default=ENOVAL, retry=True)

                if result is ENOVAL:
                    try:
                        result = await fn(*args, **kwargs)
                    except errors as exc:
                        if errors_expire is None or errors_expire > 0:
                            await call_async(
                                cache.set,
                                key,
                                CachedError(exc),
                                errors_expire,
                                tag=tag,
                                retry=True,
                            )
                        raise
                    if expire is None or expire > 0:
                        await call_async(
                            cache.set, key, result, expire, tag=tag, retry=True
                        )

                if isinstance(result, CachedError):
                    raise result.exception
                return result

            return wrapper

        # For sync functions, we can use diskcache.memoize() directly
        if errors:
            raise NotImplementedError("Caching errors is supported only for async")
        return cache.memoize(expire=expire, tag=tag, ignore=ignore)(fn)

    return decorator


class BytecodeCache(BaseBytecodeCache):
    def __init__(self, cache: Cache):
        self.cache = cache

    def load_bytecode(self, bucket: Bucket):
        try:
            bucket.bytecode_from_string(self.cache.get(f"jinja:{bucket.key}"))
        except KeyError:
            return

    def dump_bytecode(self, bucket: Bucket):
        self.cache.set(f"jinja:{bucket.key}", bucket.bytecode_to_string(), tag="jinja")


@lru_cache
def get_jinja_cache() -> BytecodeCache:
    return BytecodeCache(get_cache())
