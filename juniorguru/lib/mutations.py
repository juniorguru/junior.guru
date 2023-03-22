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


class MutationsNotInitializedError(Exception):
    pass


class MutationsNotAllowedError(Exception):
    pass


class Mutations:
    def __init__(self):
        self.allowed = set()
        self._initialized = False

    def allow(self, *service_names):
        for service_name in service_names:
            service = Services[service_name.upper()]
            self.allowed.add(service)
            logger[service_name.lower()].debug('Allowed')
        self._initialized = True

    def allow_all(self):
        for service in Services:
            self.allowed.add(service)
            logger[service.name.lower()].debug('Allowed')
        self._initialized = True

    def is_allowed(self, service_name):
        self._raise_if_not_initialized()
        return Services[service_name.upper()] in self.allowed

    def dump(self):
        """Dumps the current state of allowed mutations into a simple list. Useful for inter-process communitacion."""
        return sorted([service.name.lower() for service in self.allowed])

    def load(self, service_names):
        """Loads the state of allowed mutations from a simple list. Useful for inter-process communitacion."""
        self.allow(*service_names)

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
                    self._raise_if_not_initialized()
                    if service in self.allowed:
                        return await fn(*args, **kwargs)
                    return warn()
                return wrapper

            @wraps(fn)
            def wrapper(*args, **kwargs):
                self._raise_if_not_initialized()
                if service in self.allowed:
                    return fn(*args, **kwargs)
                return warn()
            return wrapper
        return decorator

    def _raise_if_not_initialized(self):
        if not self._initialized:
            raise MutationsNotInitializedError()


mutations = Mutations()
