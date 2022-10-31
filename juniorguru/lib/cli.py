import pkgutil
from importlib import import_module


def command_name(module_name):
    return module_name.split('.')[-1].replace('_', '-')


def load_command(module):
    return command_name(module.__name__), module.main


def import_commands(package):
    for _, name, _ in pkgutil.iter_modules(package.__path__):
        yield load_command(import_module(f"{package.__package__}.{name}"))
