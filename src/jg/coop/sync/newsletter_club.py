from datetime import date, datetime, timedelta

import click
import httpx
from discord.abc import GuildChannel
from pydantic import BaseModel

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers, months, mutations
from jg.coop.lib.buttondown import ButtondownAPI
from jg.coop.lib.cli import async_command
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.newsletter import NewsletterIssue


logger = loggers.from_path(__file__)


class PreparedMessage(BaseModel):
    channel_id: int
    content: str


@cli.sync_command(dependencies=["club-content", "pages"])
@click.option(
    "--channel-users", "users_channel_id", default="announcements", type=parse_channel
)
@click.option(
    "--channel-admin", "admin_channel_id", default="business", type=parse_channel
)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@click.option("--emoji", default="💌", type=str)
@db.connection_context()
@async_command
async def main(
    users_channel_id: int, admin_channel_id: int, today: date, emoji: str
) -> None:
    this_month = months.this_month(today)
    messages = []
    logger.info(f"Checking email drafts since {this_month}")
    async with ButtondownAPI() as api:
        data = await api.get_emails_since(this_month)
        if data["count"]:
            logger.info("Newsletter already published this month")
        else:
            data = await api.get_drafts_since(this_month)
            if data["count"]:
                logger.info("Preparing admin club post")
                messages.append(create_admin_message(emoji, admin_channel_id, data))
            else:
                logger.info("No drafts found")

    logger.info("Checking published and archived newsletters")
    newsletter = NewsletterIssue.latest()
    logger.info(f"Latest newsletter URL: {newsletter.absolute_url}")
    try:
        logger.info("Verifying newsletter page accessibility")
        response = httpx.head(newsletter.absolute_url, timeout=5.0)
        response.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning(f"Newsletter page not accessible: {e}")
    else:
        logger.info(f"Newsletter published on: {newsletter.published_on}")
        if newsletter.published_on >= (today - timedelta(days=60)):
            logger.info("Newsletter is recent enough!")
            if message := ClubMessage.last_bot_message(
                users_channel_id,
                starting_emoji=emoji,
                contains_text=newsletter.absolute_url,
            ):
                logger.info(f"Club post for users already exists: {message.url}")
            else:
                logger.info("Preparing club post for users")
                messages.append(
                    create_users_message(emoji, users_channel_id, newsletter)
                )
        else:
            logger.warning("Latest newsletter not recent enough")
    logger.debug(f"Prepared {len(messages)} messages:\n{messages!r}")
    discord_task.run(post, messages)


def create_admin_message(emoji: str, channel_id: int, data: dict) -> PreparedMessage:
    return PreparedMessage(
        channel_id=channel_id,
        content=(
            f"{emoji} Vidím nějaké rozepsané newslettery:\n"
            + "\n".join(
                (
                    f"- `{datetime.fromisoformat(email['creation_date']).date()}` "
                    f"{email['subject']} "
                    f"[Otevřít](https://buttondown.com/emails/{email['id']})"
                )
                for email in data["results"]
            )
        ),
    )


def create_users_message(
    emoji: str, channel_id: int, newsletter_issue: NewsletterIssue
) -> PreparedMessage:
    return PreparedMessage(
        channel_id=channel_id,
        content=(
            f"{emoji} Nový newsletter je venku! "
            f"**{newsletter_issue.subject}** je k přečtení tady: "
            f"{newsletter_issue.absolute_url} ({newsletter_issue.reading_time} min čtení)"
        ),
    )


@mutations.mutates_discord()
async def post(client: ClubClient, messages: list[PreparedMessage]) -> None:
    for message in messages:
        channel: GuildChannel = client.get_channel(message.channel_id)
        logger.info(f"Posting message to channel {channel.name!r}")
        await channel.send(message.content)
