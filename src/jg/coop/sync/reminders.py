from datetime import timedelta

import click
from discord import NotFound

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


# TODO
# - create reminders.yml
# - if multiple reminders with the same periodicity go to the same channel, they should be rotated by random
# - maybe its just newcomers, intro, and then we should dose tips to chat monthly?!?
REMINDERS = [
    (
        "👋",
        ClubChannelID.NEWCOMERS,
        (
            "Ahoj! Toto je speciální kanál, který vidí jen **nově příchozí** jako ty a **moderátoři**. "
            "Pokud není jasné, jak něco funguje, neboj se tady zeptat. "
            "Rádi poradíme, nasměrujeme. Žádná otázka není blbá.\n\n"
            "Každý den sem posílám jeden tip, který by měl pomoci s orientací v klubu. "
            f"Všechny najdeš tady: <#{ClubChannelID.TIPS}>"
        ),
        7,
    ),
    (
        "💡",
        ClubChannelID.INTRO,
        "Proč je dobré se představit ostatním a co vůbec napsat? Přečti si klubový tip {👋}",
        30,
    ),
    # (
    #     "💡",
    #     ClubChannelID.CHAT,
    #     "Chceš se družit a potkávat s lidmi v místě, kde žiješ? Přečti si klubový tip {👭}",
    #     30,
    # ),
]


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["tips"])
@click.option("--force", is_flag=True)
def main(force: bool):
    discord_task.run(ensure_reminders, REMINDERS, force)


@db.connection_context()
async def ensure_reminders(
    client: ClubClient,
    reminders: list[tuple[str, ClubChannelID, str, int]],
    force: bool,
):
    logger.info("Ensuring reminders")
    channel_tips = await client.fetch_channel(ClubChannelID.TIPS)
    tip_urls_by_emoji = {
        get_starting_emoji(thread.name): thread.jump_url
        for thread in channel_tips.threads
    }
    for control_emoji, channel_id, content_template, period_days in reminders:
        last_message = ClubMessage.last_bot_message(channel_id, control_emoji)
        if force:
            logger.warning("Forcing reminder!")
        elif is_message_over_period_ago(last_message, timedelta(days=period_days)):
            logger.warning(f"Last reminder is more than {period_days} old!")
        else:
            logger.info("Reminder is still fresh, skipping")
            return
        channel = await client.fetch_channel(channel_id)
        content = f"{control_emoji} {content_template.format(**tip_urls_by_emoji)}"
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
