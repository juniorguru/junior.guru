import asyncio
import pkgutil
from functools import wraps
from importlib import import_module
import threading
from types import ModuleType
from typing import Awaitable, Callable, Generator


def command_name(module_name: str) -> str:
    return module_name.split(".")[-1].replace("_", "-")


def load_command(module: ModuleType) -> tuple[str, Callable]:
    return command_name(module.__name__), module.main


def import_commands(package: ModuleType) -> Generator[tuple[str, Callable], None, None]:
    for _, name, _ in pkgutil.iter_modules(package.__path__):
        yield load_command(import_module(f"{package.__package__}.{name}"))


def async_command(fn: Callable[..., Awaitable]) -> Callable:
    @wraps(fn)
    def wrapper(*args, **kwargs):
        def run():
            asyncio.run(fn(*args, **kwargs))

        thread = threading.Thread(target=run)
        thread.start()
        thread.join()

    return wrapper
