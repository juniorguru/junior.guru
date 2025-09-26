import click

from jg.coop.cli import (
    backup,
    cache,
    cancel_previous_builds,
    channel_to_thread,
    check_bot,
    check_docs,
    check_sponsors,
    data,
    notes,
    screenshots,
    sync,
    tidy,
    web,
    winners,
)
from jg.coop.cli.dev import main as dev
from jg.coop.lib import loggers
from jg.coop.lib.cache import close_cache
from jg.coop.lib.cli import load_command


subcommands = click.Group(
    commands=dict(
        map(
            load_command,
            [
                backup,
                cache,
                cancel_previous_builds,
                channel_to_thread,
                check_bot,
                check_docs,
                check_sponsors,
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
    context.call_on_close(close)


def close():
    loggers.clear_configuration()
    close_cache()
