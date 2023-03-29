import inspect
from contextlib import contextmanager
from functools import wraps
from typing import Generator, Iterable

from juniorguru.lib import loggers
from juniorguru.lib import global_state


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
            async def wrapper(*args, **kwargs):
                if service in _get_allowed():
                    return await fn(*args, **kwargs)
                return create_error()
            return wrapper

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if service in _get_allowed():
                return fn(*args, **kwargs)
            return create_error()
        return wrapper
    return decorator


@contextmanager
def force_allow(*services) -> Generator[None, None, None]:
    dump = _get_allowed()
    try:
        services = list(map(str.lower, services))
        for service in services:
            assert service in KNOWN_SERVICES
        global_state.set('mutations.allowed', services)
        logger['force_allow'].debug(f'Force-allowed: {services!r}')
        yield
    finally:
        _set_allowed(dump)
        logger['force_allow'].debug(f'Back to: {dump!r}')
