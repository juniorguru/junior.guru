from functools import wraps

from invoke import task

from juniorguru.lib.timer import measure


def sync_task(*args, **kwargs):
    def decorator(fn):
        kwargs.setdefault('name', fn.__module__.split('.')[-1])
        @task(*args, **kwargs)
        @wraps(fn)
        def wrapper(context):
            return measure(fn)()
        return wrapper
    return decorator
