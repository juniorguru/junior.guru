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
    "google_sheets",
    "memberful",
    "openai",
    "mastodon",
]

CACHE_KEY = "mutations:allowed"


class MutationsNotAllowedError(Exception):
    def __bool__(self) -> Literal[False]:
        return False


def _get_allowed() -> set:
    return set(get_cache().get(CACHE_KEY) or [])


def _set_allowed(allowed: Iterable) -> None:
    get_cache().set(CACHE_KEY, set(allowed))


def allow(*services: str) -> None:
    allowed = _get_allowed()
    for service in map(str.lower, services):
        if service not in KNOWN_SERVICES:
            raise ValueError(f"Unknown service: {service!r} not in {KNOWN_SERVICES!r}")
        allowed.add(service)
    _set_allowed(allowed)
    logger.info(f"Allowed: {list(allowed)!r}")


def allow_all() -> None:
    allow(*KNOWN_SERVICES)


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
mutates_google_sheets = partial(mutates, "google_sheets")
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
mutating_google_sheets = partial(mutating, "google_sheets")
mutating_mastodon = partial(mutating, "mastodon")
mutating_memberful = partial(mutating, "memberful")
mutating_openai = partial(mutating, "openai")


@contextmanager
def allowing(service) -> Generator[None, None, None]:
    service = service.lower()
    assert service in KNOWN_SERVICES

    dump = _get_allowed()
    try:
        _set_allowed([service])
        logger["allowing"].debug(f"Force-allowed: {service!r}")
        yield
    finally:
        _set_allowed(dump)
        logger["allowing"].debug(f"Back to: {dump!r}")


allowing_apify = partial(allowing, "apify")
allowing_buttondown = partial(allowing, "buttondown")
allowing_discord = partial(allowing, "discord")
allowing_fakturoid = partial(allowing, "fakturoid")
allowing_google_sheets = partial(allowing, "google_sheets")
allowing_mastodon = partial(allowing, "mastodon")
allowing_memberful = partial(allowing, "memberful")
allowing_openai = partial(allowing, "openai")


_globals = globals()
for service in KNOWN_SERVICES:
    assert f"mutates_{service}" in _globals
    assert f"mutating_{service}" in _globals
    assert f"allowing_{service}" in _globals
