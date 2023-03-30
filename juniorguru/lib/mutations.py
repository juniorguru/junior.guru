import inspect
from contextlib import contextmanager
from functools import wraps, partial
from typing import Any, Generator, Iterable

from juniorguru.lib import global_state, loggers


logger = loggers.from_path(__file__)


KNOWN_SERVICES = ['discord', 'google_sheets', 'fakturoid', 'memberful']


class MutationsNotAllowedError(Exception):
    pass


def _get_allowed() -> set:
    return set(global_state.get('mutations.allowed') or [])


def _set_allowed(allowed: Iterable) -> None:
    global_state.set('mutations.allowed', list(allowed))


def allow(*services: str) -> None:
    allowed = _get_allowed()
    for service in map(str.lower, services):
        assert service in KNOWN_SERVICES
        allowed.add(service)
    _set_allowed(allowed)
    logger.info(f'Allowed: {allowed!r}')


def allow_all() -> None:
    allow(*KNOWN_SERVICES)


def is_allowed(service) -> bool:
    return service in _get_allowed()


def mutates(service, raises=False):
    service = service.lower()
    assert service in KNOWN_SERVICES

    def create_error():
        logger['mutates'].warning(f'Not allowed: {service}')
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


for service in KNOWN_SERVICES:
    globals()[f"mutates_{service}"] = partial(mutates, service)


class MutatingProxy:
    def __init__(self, service: str, object: Any, raises: bool=False):
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


for service in KNOWN_SERVICES:
    globals()[f"mutating_{service}"] = partial(mutating, service)


@contextmanager
def allowing(service) -> Generator[None, None, None]:
    service = service.lower()
    assert service in KNOWN_SERVICES

    dump = _get_allowed()
    try:
        global_state.set('mutations.allowed', [service])
        logger['allowing'].debug(f'Force-allowed: {service!r}')
        yield
    finally:
        _set_allowed(dump)
        logger['allowing'].debug(f'Back to: {dump!r}')


for service in KNOWN_SERVICES:
    globals()[f"allowing_{service}"] = partial(allowing, service)
