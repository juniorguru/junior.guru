import click

from juniorguru.cli import (cancel_previous_builds, check_docs, check_links, data,
                            participant, screenshots, students, sync, web, winners)
from juniorguru.cli.dev import main as dev
from juniorguru.lib.cli import load_command


subcommands = click.Group(commands=dict(map(load_command, [
    cancel_previous_builds,
    check_docs,
    check_links,
    web,
    data,
    participant,
    screenshots,
    winners,
    students,
    sync,
])))


main = click.CommandCollection(sources=[dev, subcommands])
