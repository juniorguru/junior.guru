import inspect
from enum import Enum, auto
from functools import wraps

from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


class Services(Enum):
    DISCORD = auto()
    GOOGLE_SHEETS = auto()
    FAKTUROID = auto()
    MEMBERFUL = auto()


class MutationsNotAllowed:
    pass


class MutationsNotAllowedError(Exception):
    pass


class Mutations:
    def __init__(self):
        self.allowed = set()

    def allow(self, service_name):
        service = Services[service_name.upper()]
        self.allowed.add(service)
        logger[service_name.lower()].info('Allowed')

    def allow_all(self):
        for service in Services:
            self.allowed.add(service)
            logger[service.name.lower()].info('Allowed')

    def is_allowed(self, service_name):
        return Services[service_name.upper()] in self.allowed

    def mutates(self, service_name, raises=False):
        service = Services[service_name.upper()]

        def warn():
            logger[service_name.lower()].warning('Not allowed')
            if raises:
                raise MutationsNotAllowedError
            return MutationsNotAllowed

        def decorator(fn):
            if inspect.iscoroutinefunction(fn):
                @wraps(fn)
                async def wrapper(*args, **kwargs):
                    if service in self.allowed:
                        return await fn(*args, **kwargs)
                    return warn()
                return wrapper

            @wraps(fn)
            def wrapper(*args, **kwargs):
                if service in self.allowed:
                    return fn(*args, **kwargs)
                return warn()
            return wrapper
        return decorator


mutations = Mutations()
