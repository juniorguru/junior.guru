import pkgutil
from importlib import import_module
from typing import cast

import click

from jg.coop.lib import loggers
from jg.coop.lib.cache import close_cache
from jg.coop.lib.cli import command_name, find_commands, import_command


class LazyGroup(click.Group):
    """Imports a subcommand's module only when that command is actually used"""

    flattened_modules = ["dev"]

    def list_commands(self, ctx: click.Context) -> list[str]:
        return sorted(find_commands(__path__, flatten=self.flattened_modules))

    def get_command(self, ctx: click.Context, name: str) -> click.Command | None:
        commands = dict(find_commands(__path__, flatten=self.flattened_modules))
        if import_path := commands.get(name):
            return import_command(ctx, name, import_path)
        return None


@click.command(cls=LazyGroup)
@click.option("--debug/--no-debug", default=None)
@click.pass_context
def main(context: click.Context, debug: bool):
    if debug:
        loggers.reconfigure_level("DEBUG")
        loggers.from_path(__file__).info("Logging level set to DEBUG")
    context.call_on_close(close)


def close():
    loggers.clear_configuration()
    close_cache()
