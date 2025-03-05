from datetime import date, datetime, timedelta

import click
import httpx

from jg.coop.cli.sync import main as cli
from jg.coop.lib import fakturoid, loggers, mutations


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@click.option("--expire-days", default=70, type=int)
def main(today: date, expire_days: int):
    token = fakturoid.auth()
    with fakturoid.get_client(token) as client:
        response = client.get("/inbox_files.json")
        response.raise_for_status()
        inbox_files: list = response.json()
        for inbox_file in inbox_files:
            updated_at = datetime.fromisoformat(inbox_file["updated_at"])
            if updated_at.date() < (today - timedelta(days=expire_days)):
                logger.warning(
                    f"File {inbox_file['filename']} is old: {updated_at.date()}"
                )
                remove_inbox_file(client, inbox_file["id"])
            else:
                logger.debug(
                    f"File {inbox_file['filename']} is ok: {updated_at.date()}"
                )


@mutations.mutates_fakturoid()
def remove_inbox_file(client: httpx.Client, inbox_file_id: int):
    logger.info(f"Removing file: ID {inbox_file_id}")
    response = client.delete(f"/inbox_files/{inbox_file_id}.json")
    response.raise_for_status()
