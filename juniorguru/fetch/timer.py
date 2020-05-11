from functools import wraps
from time import time


try:
    import pync
except (Exception, ImportError):
    pync = None


def notify(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time()
        try:
            return fn(*args, **kwargs)
        finally:
            t = time() - t0
            if pync:
                fn_name = f'{fn.__module__}.{fn.__name__}()'
                pync.Notifier.notify(f'{t / 60:.1f}min',
                                     title=f'Finished: {fn_name}')
    return wrapper
