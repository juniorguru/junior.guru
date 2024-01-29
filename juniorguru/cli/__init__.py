import click

from juniorguru.cli import (
    backup,
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
from juniorguru.cli.dev import main as dev
from juniorguru.lib.cache import close_cache
from juniorguru.lib.cli import load_command


subcommands = click.Group(
    commands=dict(
        map(
            load_command,
            [
                backup,
                cancel_previous_builds,
                check_docs,
                check_links,
                check_bot,
                web,
                data,
                tidy,
                screenshots,
                notes,
                winners,
                sync,
            ],
        )
    )
)


@click.command(cls=click.CommandCollection, sources=[dev, subcommands])
@click.pass_context
def main(context: click.Context):
    context.call_on_close(close_cache)
