from datetime import timedelta
from pathlib import Path

import click
import yaml
from discord import NotFound
from pydantic import BaseModel, field_validator

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import (
    ClubChannelID,
    ClubClient,
    get_starting_emoji,
    is_message_over_period_ago,
    parse_channel,
    resolve_references,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage


class ReminderConfig(BaseModel):
    control_emoji: str
    channel_id: ClubChannelID
    content_template: str
    period_days: int

    @field_validator("channel_id", mode="before")
    @classmethod
    def parse_channel_id(cls, value: int | str) -> int | str:
        if isinstance(value, str):
            return parse_channel(value)
        return value

    @field_validator("content_template", mode="before")
    @classmethod
    def parse_content_template(cls, value: str) -> str:
        return resolve_references(value)


class RemindersConfig(BaseModel):
    reminders: list[ReminderConfig]


logger = loggers.from_path(__file__)


def build_reminder_content(
    reminder: ReminderConfig, tip_urls_by_emoji: dict[str, str]
) -> str:
    return (
        f"-# "
        f"{reminder.control_emoji} "
        f"{reminder.content_template.format(**tip_urls_by_emoji)}"
    )


@cli.sync_command(dependencies=["tips", "club-content", "roles"])
@click.option(
    "--path",
    default=Path("src/jg/coop/data/reminders.yml"),
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--force", is_flag=True)
def main(path: Path, force: bool) -> None:
    reminders_config = RemindersConfig(**yaml.safe_load(path.read_text()))
    discord_task.run(ensure_reminders, reminders_config.reminders, force)


@db.connection_context()
async def ensure_reminders(
    client: ClubClient,
    reminders: list[ReminderConfig],
    force: bool,
) -> None:
    logger.info("Ensuring reminders")
    channel_tips = await client.fetch_channel(ClubChannelID.TIPS)
    tip_urls_by_emoji = {
        get_starting_emoji(thread.name): thread.jump_url
        for thread in channel_tips.threads
    }

    for reminder in reminders:
        last_message = ClubMessage.last_bot_message(
            reminder.channel_id, reminder.control_emoji
        )

        if force:
            logger.warning("Forcing reminder!")
        elif is_message_over_period_ago(
            last_message, timedelta(days=reminder.period_days)
        ):
            logger.warning(f"Last reminder is more than {reminder.period_days} old!")
        else:
            logger.info("Reminder is still fresh, skipping")
            return

        channel = await client.fetch_channel(reminder.channel_id)
        content = build_reminder_content(reminder, tip_urls_by_emoji)

        logger.info(f"Sending: {content!r}")
        with mutating_discord(channel) as proxy:
            await proxy.send(content, silent=True)
        if last_message:
            logger.info(f"Deleting previous reminder: {last_message.url}")
            try:
                message = await channel.fetch_message(last_message.id)
                with mutating_discord(message) as proxy:
                    await proxy.delete()
            except NotFound:
                logger.warning("Reminder not found, probably already deleted")
