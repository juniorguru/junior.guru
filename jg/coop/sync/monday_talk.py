from datetime import date

import click
from discord import ScheduledEvent

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubChannelID, ClubClient, parse_channel
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.tip import Tip


logger = loggers.from_path(__file__)


MONDAY_TALK_EMOJI = "💬"


@cli.sync_command(dependencies=["club-content", "tips"])
@click.option("--channel", "channel_id", default="announcements", type=parse_channel)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
def main(channel_id: int, today: date):
    message = ClubMessage.last_bot_message(channel_id, starting_emoji=MONDAY_TALK_EMOJI)
    if message and message.created_at.date() == today:
        logger.info("Monday talk announcement already exists")
        return

    with db.connection_context():
        tip_url = Tip.get_by_id("monday_talk").discord_url

    discord_task.run(announce_talk, channel_id, tip_url, today)


async def announce_talk(client: ClubClient, channel_id: int, tip_url: str, today: date):
    today_monday_talks = (
        talk
        for talk in client.club_guild.scheduled_events
        if talk.start_time.date() == today and is_monday_talk(talk)
    )
    try:
        monday_talk = next(today_monday_talks)
    except StopIteration:
        logger.info("No monday talk today")
        return

    logger.info(f"Announcing monday talk {monday_talk.url}")
    text = (
        f"{MONDAY_TALK_EMOJI} Jako každý týden, i dnes večer bude v klubovně [Pondělní povídání]({monday_talk.url})!\n\n"
        f"- Co čekat? Mrkni na {tip_url}"
        "\n"
        f"- Chceš něco konkrétního probrat? Piš do https://discord.com/channels/769966886598737931/1198999483309117582/1198999483309117582"
    )
    mentions = sorted([user.mention async for user in monday_talk.subscribers()])
    if mentions:
        text += f"\n\n{' '.join(mentions)} na viděnou, slyšenou večer 👋"

    channel = await client.fetch_channel(channel_id)
    with mutating_discord(channel) as proxy:
        await proxy.send(text, silent=True, suppress=True)


def is_monday_talk(scheduled_event: ScheduledEvent) -> bool:
    if scheduled_event.name.lower().strip() != "pondělní povídání":
        return False
    location_id = getattr(scheduled_event.location.value, "id", None)
    return location_id == ClubChannelID.CLUBHOUSE
