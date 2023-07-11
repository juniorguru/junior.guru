import click

from juniorguru.cli import (backup, cancel_previous_builds, check_bot, check_docs,
                            check_links, data, notes, screenshots, sync, tidy,
                            web, winners)
from juniorguru.cli.dev import main as dev
from juniorguru.lib.cli import load_command


subcommands = click.Group(commands=dict(map(load_command, [
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
])))


main = click.CommandCollection(sources=[dev, subcommands])
