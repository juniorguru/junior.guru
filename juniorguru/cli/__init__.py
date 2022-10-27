import click

from juniorguru.cli.dev import main as dev
from juniorguru.cli import (cancel_previous_builds, check_docs, check_links, data,
                            participant, screenshots, students, web, winners, sync)


class MainGroup(click.MultiCommand):
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

    def list_commands(self, context):
        return sorted([name for name, command in self.load_dynamic_commands()])

    def get_command(self, context, name):
        return dict(self.load_dynamic_commands())[name]


@click.group(cls=MainGroup)
def subcommands():
    pass


main = click.CommandCollection(sources=[dev, subcommands])
