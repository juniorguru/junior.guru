import subprocess

import click

from juniorguru.web.__main__ import main as freeze_main


@click.group()
def main():
    pass


@main.command()
def freeze():
    freeze_main()


@main.command()
def mkdocs():
    subprocess.run(['mkdocs', 'build',
                    '--config-file=juniorguru/mkdocs/mkdocs.yml',
                    '--site-dir=../../public/mkdocs'], check=True)


@main.command()
def build():
    subprocess.run(['npx', 'gulp', 'build'], check=True)


@main.command()
def serve():
    subprocess.run(['npx', 'gulp', 'serve'], check=True)
