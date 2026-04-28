from datetime import timedelta

import click
from discord import NotFound
from pydantic import BaseModel

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import (
    ClubChannelID,
    ClubClient,
    get_starting_emoji,
    is_message_over_period_ago,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage


class ReminderSpec(BaseModel):
    control_emoji: str
    channel_id: ClubChannelID
    content_template: str
    period_days: int


REMINDERS: list[ReminderSpec] = [
    ReminderSpec(
        control_emoji="👋",
        channel_id=ClubChannelID.NEWCOMERS,
        content_template=(
            "Ahoj! Toto je speciální kanál, který vidí jen **nově příchozí** jako ty a **moderátoři**. "
            "Pokud není jasné, jak něco funguje, neboj se tady zeptat. "
            "Rádi poradíme, nasměrujeme. Žádná otázka není blbá.\n\n"
            "Každý den sem posílám jeden tip, který by měl pomoci s orientací v klubu. "
            f"Všechny najdeš tady: <#{ClubChannelID.TIPS}>"
        ),
        period_days=7,
    ),
    ReminderSpec(
        control_emoji="💡",
        channel_id=ClubChannelID.INTRO,
        content_template="Proč je dobré se představit ostatním a co vůbec napsat? Přečti si klubový tip {👋}",
        period_days=30,
    ),
    # ReminderSpec(
    #     control_emoji="💡",
    #     channel_id=ClubChannelID.CHAT,
    #     content_template="Chceš se družit a potkávat s lidmi v místě, kde žiješ? Přečti si klubový tip {👭}",
    #     period_days=30,
    # ),
]


logger = loggers.from_path(__file__)


def build_reminder_content(
    reminder: ReminderSpec, tip_urls_by_emoji: dict[str, str]
) -> str:
    return (
        f"{reminder.control_emoji} "
        f"{reminder.content_template.format(**tip_urls_by_emoji)}"
    )


@cli.sync_command(dependencies=["tips"])
@click.option("--force", is_flag=True)
def main(force: bool) -> None:
    discord_task.run(ensure_reminders, REMINDERS, force)


@db.connection_context()
async def ensure_reminders(
    client: ClubClient,
    reminders: list[ReminderSpec],
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
            await proxy.send(content)
        if last_message:
            logger.info(f"Deleting previous reminder: {last_message.url}")
            try:
                message = await channel.fetch_message(last_message.id)
                with mutating_discord(message) as proxy:
                    await proxy.delete()
            except NotFound:
                logger.warning("Reminder not found, probably already deleted")
