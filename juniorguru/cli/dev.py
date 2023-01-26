import subprocess
from pathlib import Path

import click
import pytest
from ghp_import import ghp_import

from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED, run_discord_task


DATA_DIR = 'juniorguru/data'

BACKUP_FILE = 'backup.tar.gz'


logger = loggers.from_path(__file__)


@click.group()
def main():
    pass


@main.command()
@click.option('--pull/--no-pull', default=True)
def install(pull):
    try:
        if pull:
            subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], check=True)
        subprocess.run(['poetry', 'install'], check=True)
        subprocess.run(['playwright', 'install', 'firefox'], check=True)
        subprocess.run(['npm', 'ci'], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
def lint():
    try:
        subprocess.run(['flake8'], check=True)
        subprocess.run(['npx', 'stylelint',
                        'juniorguru/scss/**/*.*css',
                        'juniorguru/image_templates/*.*css'], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
@click.argument('path', type=click.Path(exists=True, type=Path))
def format(path):
    try:
        subprocess.run(['isort', str(path)], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command(context_settings={'ignore_unknown_options': True})
@click.argument('pytest_args', nargs=-1, type=click.UNPROCESSED)
def test(pytest_args):
    code = pytest.main(list(pytest_args))
    if code:
        raise click.Abort()


@main.command()
@click.option('--data-dir', default=DATA_DIR, type=click.Path(path_type=Path, exists=True, file_okay=False))
@click.option('--backup-file', default=BACKUP_FILE, type=click.Path(path_type=Path, exists=False, dir_okay=False))
@click.option('--discord/--no-discord', default=DISCORD_MUTATIONS_ENABLED)
@click.option('--discord-template', default='jg-backup')
def backup(data_dir, backup_file, discord, discord_template):
    logger['backup'].info(f'Backing up {data_dir} to {backup_file}')
    subprocess.run(['tar', '-cvzf', backup_file, data_dir], check=True)
    logger['backup'].info(f'Done! {backup_file.stat().st_size / 1048576:.0f} MB')
    if discord:
        logger['backup'].info('Backing up Discord')
        run_discord_task('juniorguru.cli.dev.backup_discord_task', discord_template)
    else:
        logger['backup'].info('Discord backup not enabled')


async def backup_discord_task(client, template_name):
    try:
        logger['backup'].info(f'Looking for template {template_name}')
        template = [template for template in (await client.juniorguru_guild.templates())
                    if template.name == template_name][0]
    except IndexError:
        logger['backup'].warning(f'Not found! Creating template {template_name}')
        await client.juniorguru_guild.create_template(name=template_name)
    else:
        logger['backup'].info(f'Syncing template {template_name}')
        await template.sync()


@main.command()
@click.argument('commit_hash', envvar='CIRCLE_SHA1')
@click.argument('build_url', envvar='CIRCLE_BUILD_URL')
def deploy(commit_hash, build_url):
    message = f'deploy {commit_hash} 🐣 [skip ci]\n\n{build_url}'
    ghp_import('public', mesg=message, push=True, cname='junior.guru', nojekyll=True)


@main.command()
def reset_repo():
    try:
        subprocess.run(['git', 'reset', '--hard'], check=True)
        subprocess.run(['git', 'clean', '-f', '-d'], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True, type=Path))
@click.option('--message', default='save changes 🛠️')
@click.option('--build-url', envvar='CIRCLE_BUILD_URL')
@click.option('--skip-ci/--no-skip-ci', default=True)
def save_changes(paths, message, build_url, skip_ci):
    if skip_ci:
        message += ' [skip ci]'
    if build_url:
        message += f'\n\n{build_url}'
    try:
        for path in paths:
            logger['save-changes'].info(f'Adding path: {path}')
            subprocess.run(['git', 'add', '-A', str(path)], check=True)

        if subprocess.run(['git', 'diff', '--name-only', '--cached']).stdout:
            logger['save-changes'].info(f'Commit message: {message!r}')
            subprocess.run(['git', 'commit', '-m', message], check=True)
            logger['save-changes'].info('Pushing changes')
            subprocess.run(['git', 'push'], check=True)
        else:
            logger['save-changes'].warning('No changes to push')
    except subprocess.CalledProcessError:
        raise click.Abort()
