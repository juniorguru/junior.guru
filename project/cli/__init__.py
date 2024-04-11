import click

from project.cli import (
    backup,
    cache,
    cancel_previous_builds,
    check_bot,
    check_docs,
    check_links,
    data,
    notes,
    screenshots,
    sync,
    tidy,
    web,
    winners,
)
from project.cli.dev import main as dev
from project.lib import loggers
from project.lib.cache import close_cache
from project.lib.cli import load_command


subcommands = click.Group(
    commands=dict(
        map(
            load_command,
            [
                backup,
                cache,
                cancel_previous_builds,
                check_bot,
                check_docs,
                check_links,
                data,
                notes,
                screenshots,
                sync,
                tidy,
                web,
                winners,
            ],
        )
    )
)


@click.command(cls=click.CommandCollection, sources=[dev, subcommands])
@click.option("--debug/--no-debug", default=None)
@click.pass_context
def main(context: click.Context, debug: bool):
    if debug:
        loggers.reconfigure_level("DEBUG")
        loggers.from_path(__file__).info("Logging level set to DEBUG")
    context.call_on_close(close_cache)
