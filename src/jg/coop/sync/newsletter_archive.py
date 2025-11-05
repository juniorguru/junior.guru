import json
from datetime import date, datetime
from pathlib import Path

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.buttondown import ButtondownAPI
from jg.coop.lib.cli import async_command
from jg.coop.models.base import db
from jg.coop.models.newsletter import NewsletterIssue


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option(
    "--archive-dir",
    default=Path("src/jg/coop/data/newsletter"),
    type=click.Path(path_type=Path, file_okay=False, writable=True),
)
@click.option(
    "--today", default=lambda: date.today().isoformat(), type=date.fromisoformat
)
@db.connection_context()
@async_command
async def main(archive_dir: Path, today: date):
    archive_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Newsletter archive: {archive_dir}")

    logger.info("Fetching newsletter issues from Buttondown")
    async with ButtondownAPI() as api:
        async for email_data in api.get_emails_before(today):
            logger.info(f"Fetched {email_data['absolute_url']}")
            published_on = datetime.fromisoformat(email_data["publish_date"]).date()
            path = archive_dir / f"{published_on}.json"
            path.write_text(json.dumps(email_data, ensure_ascii=False, indent=2))
            logger.info(f"Archived as {path}")

    logger.info("Saving published issues to database")
    NewsletterIssue.drop_table()
    NewsletterIssue.create_table()
    for path in sorted(archive_dir.glob("*.json")):
        logger.info(f"Reading {path}")
        data = json.loads(path.read_text())
        newsletter_issue = NewsletterIssue.from_buttondown(data)
        newsletter_issue.save()
        logger.info(f"Saved as {newsletter_issue!r}")
    logger.info(f"Done, {NewsletterIssue.count()} issues saved")
