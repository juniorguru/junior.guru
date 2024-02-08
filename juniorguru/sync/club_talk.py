from datetime import date

import click
from discord import ScheduledEvent

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_task, loggers
from juniorguru.lib.discord_club import ClubChannelID, ClubClient, parse_channel
from juniorguru.lib.mutations import mutating_discord
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.tip import Tip


logger = loggers.from_path(__file__)


TALK_EMOJI = "💬"


@cli.sync_command(dependencies=["club-content", "club-tips"])
@click.option("--channel", "channel_id", default="announcements", type=parse_channel)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
def main(channel_id: int, today: date):
    message = ClubMessage.last_bot_message(channel_id, starting_emoji=TALK_EMOJI)
    if message and message.created_at.date() == today:
        logger.info("Talk announcement already exists")
        return

    with db.connection_context():
        tip_url = Tip.get_by_id("talk").club_url

    discord_task.run(announce_talk, channel_id, tip_url, today)


async def announce_talk(client: ClubClient, channel_id: int, tip_url: str, today: date):
    talks = filter(is_talk, client.club_guild.scheduled_events)
    talks = filter(lambda talk: talk.start_time.date() == today, talks)
    try:
        talk = next(talks)
    except StopIteration:
        logger.info("No talk today")
        return

    logger.info(f"Announcing talk {talk.url}")
    text = (
        f"{TALK_EMOJI} Jako každý týden, i dnes večer bude v klubovně [Pondělní povídání]({talk.url})!\n\n"
        f"- Co čekat? Mrkni na {tip_url}"
        "\n"
        f"- Chceš něco konkrétního probrat? Piš do https://discord.com/channels/769966886598737931/1198999483309117582/1198999483309117582"
    )
    mentions = sorted([user.mention async for user in talk.subscribers()])
    if mentions:
        text += f"\n\n{' '.join(mentions)} na viděnou, slyšenou večer 👋"

    channel = await client.fetch_channel(channel_id)
    with mutating_discord(channel) as proxy:
        await proxy.send(text, silent=True, suppress=True)


def is_talk(scheduled_event: ScheduledEvent) -> bool:
    location_id = getattr(scheduled_event.location.value, "id", None)
    return location_id == ClubChannelID.CLUBHOUSE
