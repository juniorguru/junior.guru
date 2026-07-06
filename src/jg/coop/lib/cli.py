import asyncio
import pkgutil
import threading
from functools import wraps
from importlib import import_module
from types import ModuleType
from typing import Awaitable, Callable, Generator

import click


def command_name(module_name: str) -> str:
    return module_name.split(".")[-1].replace("_", "-")


def load_command(module: ModuleType) -> tuple[str, Callable]:
    return command_name(module.__name__), module.main


def import_command(
    context: click.Context, name: str, import_path: str
) -> click.Command:
    module = import_module(import_path)
    if name == command_name(module.__name__):
        return module.main
    # assuming main is a flattened click.Group
    return main.get_command(context, name)


def find_commands(
    package: str | ModuleType, flatten: list[str] | None = None
) -> Generator[tuple[str, str], None, None]:
    try:
        package_path = package.__path__
    except AttributeError:
        package_path = str(package)
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        import_path = f"{package_path}.{module_name}"
        if flatten and module_name in flatten:
            group: click.Group = import_module(import_path).main
            for command_name_ in group.list_commands(None):
                yield command_name_, import_path
        else:
            yield (command_name(module_name), import_path)


def import_commands(package: ModuleType) -> Generator[tuple[str, Callable], None, None]:
    for _, module_name in find_commands(package):
        yield load_command(import_module(module_name))


def async_command(fn: Callable[..., Awaitable]) -> Callable:
    @wraps(fn)
    def wrapper(*args, **kwargs):
        exc = None

        def run():
            try:
                asyncio.run(fn(*args, **kwargs))
            except Exception as e:
                nonlocal exc
                exc = e

        thread = threading.Thread(target=run)
        thread.start()
        thread.join()

        if exc is not None:
            raise exc

    return wrapper
