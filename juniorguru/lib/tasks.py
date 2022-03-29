import importlib
from functools import wraps
from time import perf_counter

from invoke import task

from juniorguru.lib import loggers

try:
    import pync
except (Exception, ImportError):
    pync = None


logger = loggers.get(__name__)


def import_sync_tasks(module_paths):
    return [importlib.import_module(module_path).main
            for module_path in module_paths]


def sync_task(*args, **kwargs):
    def decorator(fn):
        kwargs.setdefault('name', fn.__module__.split('.')[-1])
        @task(*args, **kwargs)
        @wraps(fn)
        def wrapper(context):
            fn_name = f'{fn.__module__}.{fn.__qualname__}'
            logger.info(f"Starting '{kwargs['name']}' ({fn_name}())")
            t0 = perf_counter()
            try:
                return fn()
            finally:
                t = perf_counter() - t0
                logger.info(f"Finished '{kwargs['name']}' ({t / 60:.1f}min)")
        return wrapper
    return decorator


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
