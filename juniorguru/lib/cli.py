import asyncio
import pkgutil
from functools import wraps
from importlib import import_module
from types import ModuleType
from typing import Awaitable, Callable, Generator

import nest_asyncio


def command_name(module_name: str) -> str:
    return module_name.split(".")[-1].replace("_", "-")


def load_command(module: ModuleType) -> tuple[str, Callable]:
    return command_name(module.__name__), module.main


def import_commands(package: ModuleType) -> Generator[tuple[str, Callable], None, None]:
    for _, name, _ in pkgutil.iter_modules(package.__path__):
        yield load_command(import_module(f"{package.__package__}.{name}"))


def async_command(fn: Callable[..., Awaitable]) -> Callable:
    # Use https://docs.python.org/3/library/asyncio-runner.html#asyncio.Runner
    # in the future?
    nest_asyncio.apply()

    @wraps(fn)
    def wrapper(*args, **kwargs):
        return asyncio.run(fn(*args, **kwargs))

    return wrapper
