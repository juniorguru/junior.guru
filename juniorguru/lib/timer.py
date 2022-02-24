from functools import wraps
from time import perf_counter

from juniorguru.lib import loggers


try:
    import pync
except (Exception, ImportError):
    pync = None


logger = loggers.get(__name__)


def notify(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            t = perf_counter() - t0
            print('\a', end='', flush=True)
            if pync:
                fn_name = f'{fn.__module__}.{fn.__qualname__}()'
                pync.Notifier.notify(f'{t / 60:.1f}min',
                                     title=f'Finished: {fn_name}')
    return wrapper


def measure(name=None):
    def decorator(fn):
        fn_name = name or f'{fn.__module__}.{fn.__qualname__}'
        @wraps(fn)
        def wrapper(*args, **kwargs):
            t0 = perf_counter()
            try:
                return fn(*args, **kwargs)
            finally:
                t = perf_counter() - t0
                logger.info(f'{fn_name}() took {t / 60:.1f}min')
        return wrapper
    return decorator
