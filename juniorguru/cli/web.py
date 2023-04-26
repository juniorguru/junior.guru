import subprocess

import click
from mkdocs.__main__ import build_command as mkdocs_build

from juniorguru.web.__main__ import main as freeze_main


@click.group()
def main():
    pass


@main.command()
def freeze():
    freeze_main()


@main.command()
@click.pass_context
def mkdocs(context):
    context.invoke(mkdocs_build, config_file='juniorguru/mkdocs/mkdocs.yml',
                                 site_dir='../../public/mkdocs')


@main.command()
def build():
    subprocess.run(['npx', 'gulp', 'build'], check=True)


@main.command()
def serve():
    subprocess.run(['npx', 'gulp', 'serve'], check=True)
