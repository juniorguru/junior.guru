import inspect
from contextlib import contextmanager
from functools import partial, wraps
from typing import Any, Generator, Iterable, Literal

from jg.coop.lib import loggers
from jg.coop.lib.cache import get_cache


logger = loggers.from_path(__file__)


KNOWN_SERVICES = [
    "apify",
    "buttondown",
    "discord",
    "fakturoid",
    "mastodon",
    "memberful",
    "openai",
]

CACHE_KEY = "__mutations__"
_CACHE_MISSING = object()


class MutationsNotAllowedError(Exception):
    def __bool__(self) -> Literal[False]:
        return False


def _get_allowed() -> set:
    return set(get_cache().get(CACHE_KEY) or [])


def _set_allowed(allowed: Iterable) -> None:
    cache = get_cache()
    if allowed_set := set(allowed):
        cache.set(CACHE_KEY, allowed_set)
    else:
        cache.delete(CACHE_KEY)


def allow(*services: str, _under_test: bool = False) -> set[str]:
    services = set(map(str.lower, services))
    if not services:
        raise ValueError("At least one service must be allowed")
    if unknown_services := (services - set(KNOWN_SERVICES)):
        raise ValueError(
            f"Unknown services: {unknown_services!r} not in {KNOWN_SERVICES!r}"
        )

    cache = get_cache()
    with cache.transact(retry=True):
        if (
            not _under_test
            and cache.get(CACHE_KEY, default=_CACHE_MISSING) is not _CACHE_MISSING
        ):
            raise RuntimeError("Mutations are already configured")
        cache.set(CACHE_KEY, services)

    logger.info(f"Allowed: {list(services)!r}")
    return services


def allow_none() -> None:
    _set_allowed([])
    logger.debug("Allowed: []")


def is_allowed(service) -> bool:
    return service in _get_allowed()


def mutates(service, raises=False):
    service = service.lower()
    assert service in KNOWN_SERVICES

    def create_error():
        logger["mutates"].warning(f"Not allowed: {service}")
        error = MutationsNotAllowedError()
        if raises:
            raise error
        return error

    def decorator(fn):
        if inspect.iscoroutinefunction(fn):

            @wraps(fn)
            async def wrapper(*args, **kwargs) -> Any | MutationsNotAllowedError:
                if service in _get_allowed():
                    return await fn(*args, **kwargs)
                return create_error()

            return wrapper

        @wraps(fn)
        def wrapper(*args, **kwargs) -> Any | MutationsNotAllowedError:
            if service in _get_allowed():
                return fn(*args, **kwargs)
            return create_error()

        return wrapper

    return decorator


mutates_apify = partial(mutates, "apify")
mutates_buttondown = partial(mutates, "buttondown")
mutates_discord = partial(mutates, "discord")
mutates_fakturoid = partial(mutates, "fakturoid")
mutates_mastodon = partial(mutates, "mastodon")
mutates_memberful = partial(mutates, "memberful")
mutates_openai = partial(mutates, "openai")


class MutatingProxy:
    def __init__(self, service: str, object: Any, raises: bool = False):
        self.service = service
        self.object = object
        self.raises = raises

    def __getattr__(self, attr) -> Any | MutationsNotAllowedError:
        attribute = getattr(self.object, attr)
        if inspect.ismethod(attribute):
            decorator = mutates(self.service, raises=self.raises)
            return decorator(attribute)
        return attribute


@contextmanager
def mutating(*args, **kwargs) -> Generator[MutatingProxy, None, None]:
    yield MutatingProxy(*args, **kwargs)


mutating_apify = partial(mutating, "apify")
mutating_buttondown = partial(mutating, "buttondown")
mutating_discord = partial(mutating, "discord")
mutating_fakturoid = partial(mutating, "fakturoid")
mutating_mastodon = partial(mutating, "mastodon")
mutating_memberful = partial(mutating, "memberful")
mutating_openai = partial(mutating, "openai")


_globals = globals()
for service in KNOWN_SERVICES:
    assert f"mutates_{service}" in _globals
    assert f"mutating_{service}" in _globals
