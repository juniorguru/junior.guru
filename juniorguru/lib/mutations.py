import inspect
from enum import Enum, auto

from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


class Services(Enum):
    DISCORD = auto()
    GOOGLE_SHEETS = auto()
    FAKTUROID = auto()
    MEMBERFUL = auto()


class MutationsNotAllowed:
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

    def mutation(self, service_name, fn):
        service = Services[service_name.upper()]
        if service in self.allowed:
            return fn

        def sync_warn(*args, **kwargs):
            logger[service_name.lower()].warning('Not allowed')
            return MutationsNotAllowed

        async def async_warn(*args, **kwargs):
            return sync_warn()

        return async_warn if inspect.iscoroutinefunction(fn) else sync_warn

    def mutates(self, service_name):
        def decorator(fn):
            return self.mutation(service_name, fn)
        return decorator


mutations = Mutations()
