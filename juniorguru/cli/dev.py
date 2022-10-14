import subprocess

import pytest
import click


@click.command()
def lint():
    try:
        subprocess.run(['flake8'], check=True)
        subprocess.run(['npx', 'stylelint',
                        'juniorguru/scss/**/*.*css',
                        'juniorguru/image_templates/*.*css'], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@click.command()
def format():
    try:
        subprocess.run(['isort', '.'], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@click.command(context_settings={'ignore_unknown_options': True})
@click.argument('pytest_args', nargs=-1, type=click.UNPROCESSED)
def test(pytest_args):
    code = pytest.main(list(pytest_args))
    if code:
        raise click.Abort()
