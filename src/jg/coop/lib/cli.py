import asyncio
import pkgutil
import threading
from collections.abc import Awaitable, Callable, Generator
from functools import wraps
from importlib import import_module
from types import ModuleType

import click


def command_name(module_name: str) -> str:
    return module_name.rsplit(".", maxsplit=1)[-1].replace("_", "-")


def import_command(name: str, import_path: str) -> click.Command:
    module = import_module(import_path)
    if name == command_name(module.__name__):
        return module.main
    # assuming main is a flattened click.Group
    return module.main.get_command(None, name)


def find_commands(
    package: str | ModuleType, flatten: list[str] | None = None
) -> Generator[tuple[str, str]]:
    if isinstance(package, str):
        package = import_module(package)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        import_path = f"{package.__name__}.{module_name}"
        if flatten and module_name in flatten:
            group: click.Group = import_module(import_path).main
            for command_name_ in group.list_commands(None):
                yield command_name_, import_path
        else:
            yield (command_name(module_name), import_path)


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
