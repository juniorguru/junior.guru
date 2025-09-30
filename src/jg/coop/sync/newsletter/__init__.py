from datetime import date, timedelta
from pathlib import Path
from pprint import pformat

import click
from jinja2 import Template

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.buttondown import ButtondownAPI
from jg.coop.lib.cli import async_command
from jg.coop.lib.template_filters import thousands
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage, ClubTopic, ClubUser
from jg.coop.models.followers import Followers


MONTH_NAMES = [
    "leden",
    "únor",
    "březen",
    "duben",
    "květen",
    "červen",
    "červenec",
    "srpen",
    "září",
    "říjen",
    "listopad",
    "prosinec",
]


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["summary"])
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="Force creating even if there are already emails this month",
)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@db.connection_context()
@async_command
async def main(force: bool, today: date):
    this_month = today.replace(day=1)
    prev_month = (this_month - timedelta(days=1)).replace(day=1)
    prev_prev_month = (prev_month - timedelta(days=1)).replace(day=1)

    async with ButtondownAPI() as api:
        logger.info(f"Checking existing emails since {this_month:%Y-%m-%d}")
        emails_count = (await api.get_emails_since(this_month))["count"]
        if emails_count:
            if force:
                logger.warning(
                    "Forcing email creation even though there are already emails this month!"
                )
            else:
                logger.warning(
                    "There are emails created this month. Skipping newsletter! Check https://buttondown.com/emails"
                )
                return

        logger.info("Preparing email data")
        month_name = MONTH_NAMES[today.month - 1]
        subscribers_count = Followers.get_latest("newsletter").count
        subscribers_new_count = (
            Followers.breakdown(this_month)["newsletter"] -
            Followers.breakdown(prev_prev_month)["newsletter"]
        )
        club_content_size = ClubMessage.content_size_by_month(prev_month)

        logger.info("Rendering email body")
        template = Template(Path(__file__).with_name("newsletter.jinja").read_text())
        email_data = {
            "subject": f"Novinky ze světa IT juniorů 🐣 {month_name} {today.year}",
            "body": template.render(
                members_count=ClubUser.members_count(),
                month_name=month_name,
                subscribers_count=subscribers_count,
                subscribers_new_count=subscribers_new_count,
                club_content_size=thousands(club_content_size),
                topics=ClubTopic.listing(),
            ),
            "status": "draft",
        }
        logger.debug(f"Email data:\n{pformat(email_data)}")

        logger.info("Creating draft")
        if data := await api.create_draft(email_data):
            logger.info(
                f"Email created!\nEdit: https://buttondown.com/emails/{data['id']}\nPreview: {data['absolute_url']}"
            )
