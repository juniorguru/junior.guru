import subprocess
from pathlib import Path

import click

from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.mutations import mutations


logger = loggers.from_path(__file__)


def op(item):
    try:
        proc = subprocess.run(['op', 'item', 'get', item,
                               '--fields', 'label=password'],
                              stdout=subprocess.PIPE,
                              check=True)
        return proc.stdout.decode('utf-8')
    except FileNotFoundError:
        return None


@click.group()
def main():
    pass


@main.command()
@click.option('--data-dir', default='juniorguru/data', type=click.Path(path_type=Path, exists=True, file_okay=False))
@click.option('--backup-file', default='backup.tgz', type=click.Path(path_type=Path, exists=False, dir_okay=False))
def data(data_dir, backup_file):
    logger.info(f'Backing up {data_dir} to {backup_file}')
    subprocess.run(['tar', '-cvzf', backup_file, data_dir], check=True)
    logger.info(f'Done! {backup_file.stat().st_size / 1048576:.0f} MB')


@main.command()
@click.option('--backup-file', default='backup.tgz', type=click.Path(path_type=Path, exists=False, dir_okay=False))
@click.option('--passphrase', envvar='BACKUP_PASSPHRASE')
@click.option('--op-item', default='Passphrase for junior.guru backup')
def encrypt(backup_file, passphrase, op_item):
    passphrase = passphrase or op(op_item) or click.prompt('Passphrase', hide_input=True)
    encrypted_file = Path(f"{backup_file}.gpg")
    logger.info(f'Encrypting {backup_file} as {encrypted_file}')
    subprocess.run(['gpg',
                    '-z', '0',  # no compression
                    '--batch',  # non-interactive
                    '--passphrase', passphrase,
                    '--symmetric',
                    '--output', encrypted_file,
                    backup_file], check=True)
    logger.info(f'Done! {encrypted_file.stat().st_size / 1048576:.0f} MB')


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
