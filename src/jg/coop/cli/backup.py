import re
import subprocess
from pathlib import Path

import click
from pycircleci.api import Api

from jg.coop.lib import discord_task, loggers, mutations
from jg.coop.lib.discord_club import ClubClient


logger = loggers.from_path(__file__)


def op(item):
    try:
        proc = subprocess.run(
            ["op", "item", "get", item, "--fields", "label=password"],
            stdout=subprocess.PIPE,
            check=True,
        )
        return proc.stdout.decode("utf-8").strip()
    except FileNotFoundError:
        return None


@click.group()
def main():
    pass


@main.command()
@click.option(
    "--data-dir",
    default="jg/coop/data",
    type=click.Path(path_type=Path, exists=True, file_okay=False),
)
@click.option(
    "--backup-file",
    default="backup.tgz",
    type=click.Path(path_type=Path, exists=False, dir_okay=False),
)
def data(data_dir, backup_file):
    logger.info(f"Backing up {data_dir} to {backup_file}")
    subprocess.run(["tar", "-cvzf", backup_file, data_dir], check=True)
    logger.info(f"Done! {backup_file.stat().st_size / 1048576:.0f} MB")


@main.command()
@click.option(
    "--backup-file",
    default="backup.tgz",
    type=click.Path(path_type=Path, exists=False, dir_okay=False),
)
@click.option("--passphrase", envvar="BACKUP_PASSPHRASE")
@click.option("--op-item", default="Passphrase for junior.guru backup")
def encrypt(backup_file, passphrase, op_item):
    passphrase = (
        passphrase or op(op_item) or click.prompt("Passphrase", hide_input=True)
    )
    encrypted_file = Path(f"{backup_file}.gpg")
    logger.info(f"Encrypting {backup_file} as {encrypted_file}")
    try:
        subprocess.run(
            [
                "gpg",
                "-z0",  # no compression
                "--batch",  # non-interactive
                "--passphrase",
                passphrase,
                "--symmetric",
                f"--output={encrypted_file}",
                backup_file,
            ],
            check=True,
        )
        logger.info(f"Done! {encrypted_file.stat().st_size / 1048576:.0f} MB")
    except subprocess.CalledProcessError:
        logger.error("Calling gpg failed!")


@main.command()
@click.argument("circleci_workflow")
@click.option("--circleci-api-key", envvar="CIRCLECI_API_KEY")
def download(circleci_workflow, circleci_api_key):
    circleci = Api(token=circleci_api_key)
    if match := re.search(r"/workflows/([^/]+)", circleci_workflow):
        workflow_id = match.group(1)
    else:
        workflow_id = circleci_workflow

    jobs = circleci.get_workflow_jobs(workflow_id, paginate=True)
    try:
        backup_job = next(job for job in jobs if job["name"] == "backup")
    except StopIteration:
        logger.error("The workflow has no backup job")
        raise click.Abort()

    artifacts = circleci.get_artifacts(
        "juniorguru", "junior.guru", backup_job["job_number"]
    )
    try:
        backup_artifact = next(
            artifact
            for artifact in artifacts
            if artifact["path"].split(".")[0] == "backup"
        )
    except StopIteration:
        logger.error("The job has no backup artifact")
        raise click.Abort()

    logger.info(f"Downloading {backup_artifact['url']}")
    artifact_file = Path(circleci.download_artifact(backup_artifact["url"]))
    logger.info(f"Done! {artifact_file.stat().st_size / 1048576:.0f} MB")


@main.command()
@click.option(
    "--encrypted-file",
    default="backup.tgz.gpg",
    type=click.Path(path_type=Path, exists=True, dir_okay=False),
)
@click.option(
    "--backup-file",
    default="backup.tgz",
    type=click.Path(path_type=Path, exists=False, dir_okay=False),
)
@click.option("--passphrase", envvar="BACKUP_PASSPHRASE")
@click.option("--op-item", default="Passphrase for junior.guru backup")
def decrypt(encrypted_file, backup_file, passphrase, op_item):
    passphrase = (
        passphrase or op(op_item) or click.prompt("Passphrase", hide_input=True)
    )
    logger.info(f"Decrypting {encrypted_file} as {backup_file}")
    try:
        subprocess.run(
            [
                "gpg",
                "--decrypt",
                "--batch",  # non-interactive
                f"--passphrase={passphrase}",
                f"--output={backup_file}",
                encrypted_file,
            ],
            check=True,
        )
        logger.info(f"Done! {backup_file.stat().st_size / 1048576:.0f} MB")
    except subprocess.CalledProcessError:
        logger.error("Calling gpg failed!")


@main.command()
@click.option("--template", default="jg-backup")
def discord(template):
    mutations.allow("discord")
    discord_task.run(backup_discord, template)


async def backup_discord(client: ClubClient, template_name):
    try:
        logger.info(f"Looking for template {template_name}")
        template = [
            template
            for template in (await client.club_guild.templates())
            if template.name == template_name
        ][0]
    except IndexError:
        logger.warning(f"Not found! Creating template {template_name}")
        await client.club_guild.create_template(name=template_name)
    else:
        logger.info(f"Syncing template {template_name}")
        await template.sync()
