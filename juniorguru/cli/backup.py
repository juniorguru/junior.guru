import subprocess
from pathlib import Path

import click

from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.mutations import mutations


logger = loggers.from_path(__file__)


@click.group()
def main():
    pass


@main.command()
@click.option('--data-dir', default='juniorguru/data', type=click.Path(path_type=Path, exists=True, file_okay=False))
@click.option('--backup-file', default='backup.tgz', type=click.Path(path_type=Path, exists=False, dir_okay=False))
@click.option('--discord/--no-discord', default=False)
def data(data_dir, backup_file, discord, ):
    logger.info(f'Backing up {data_dir} to {backup_file}')
    subprocess.run(['tar', '-cvzf', backup_file, data_dir], check=True)
    logger.info(f'Done! {backup_file.stat().st_size / 1048576:.0f} MB')


@main.command()
@click.option('--template', default='jg-backup')
def discord(template):
    mutations.allow('discord')
    discord_sync.run(backup_discord, template)


async def backup_discord(client, template_name):
    try:
        logger.info(f'Looking for template {template_name}')
        template = [template for template in (await client.club_guild.templates())
                    if template.name == template_name][0]
    except IndexError:
        logger.warning(f'Not found! Creating template {template_name}')
        await client.club_guild.create_template(name=template_name)
    else:
        logger.info(f'Syncing template {template_name}')
        await template.sync()
