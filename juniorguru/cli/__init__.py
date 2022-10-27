import click

from juniorguru.lib.cli import BaseGroup
from juniorguru.cli.dev import main as dev
from juniorguru.cli import (cancel_previous_builds, check_docs, check_links, data,
                            participant, screenshots, students, web, winners, sync)


class Group(BaseGroup):
    def load_dynamic_commands(self):
        for module in [cancel_previous_builds,
                       check_docs,
                       check_links,
                       web,
                       data,
                       participant,
                       screenshots,
                       winners,
                       students,
                       sync]:
            yield module.__name__.split('.')[-1].replace('_', '-'), module.main


@click.group(cls=Group)
def subcommands():
    pass


main = click.CommandCollection(sources=[dev, subcommands])
