from datetime import date
from pprint import pformat

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.buttondown import ButtondownAPI
from jg.coop.lib.cli import async_command
from jg.coop.models.base import db


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["summary"])
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@db.connection_context()
@async_command
async def main(today: date):
    month_starts_on = today.replace(day=1)

    async with ButtondownAPI() as api:
        logger.info(f"Checking existing emails since {month_starts_on:%Y-%m-%d}")
        emails_count = (await api.get_emails_since(month_starts_on))["count"]
        if emails_count:
            logger.warning("There are emails created this month. Skipping newsletter! Check https://buttondown.com/emails")
            return

        logger.info("Creating newsletter")
        email_data = {
            "subject": "The subject line for the email",
            "body": "This is an example of the **body** of an email.",
            "status": "draft",
        }
        logger.debug(f"Email data:\n{pformat(email_data)}")
        print(await api.create_draft(email_data))
