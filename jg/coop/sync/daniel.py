from datetime import date, timedelta

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import (
    ClubClient,
    ClubMemberID,
    get_or_create_dm_channel,
    is_message_older_than,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage, ClubUser


CZECH_WEEKDAYS = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content"])
def main():
    discord_task.run(send_daily_report)


@db.connection_context()
async def send_daily_report(client: ClubClient):
    member = await client.club_guild.fetch_member(ClubMemberID.DANIEL)
    channel = await get_or_create_dm_channel(member)

    if channel is None:
        logger.error("Couldn't get the DM channel")
        # This is not a critical task, so exit silently.
        # If this raised click.Abort() the whole sync (i.e. production build) would fail.
        return

    last_message = ClubMessage.last_bot_message(channel.id, "📊")
    yesterday = date.today() - timedelta(days=1)

    if is_message_older_than(last_message, yesterday):
        czech_weekday = CZECH_WEEKDAYS[yesterday.weekday()]

        daniel = ClubUser.get_by_id(ClubMemberID.DANIEL)
        daniel_messages = [
            message
            for message in daniel.list_public_messages
            if message.created_at.date() == yesterday
        ]
        daniel_channels = set(message.parent_channel_id for message in daniel_messages)
        daniel_threads = set(message.channel_id for message in daniel_messages)
        daniel_content_size = sum(message.content_size for message in daniel_messages)

        daniel_all_messages = [
            message
            for message in daniel.list_messages
            if message.created_at.date() == yesterday
        ]
        daniel_all_channels = set(
            message.parent_channel_id for message in daniel_all_messages
        )
        daniel_all_threads = set(message.channel_id for message in daniel_all_messages)
        daniel_all_content_size = sum(
            message.content_size for message in daniel_all_messages
        )

        honza = ClubUser.get_by_id(ClubMemberID.HONZA)
        honza_messages = [
            message
            for message in honza.list_public_messages
            if message.created_at.date() == yesterday
        ]
        honza_content_size = sum(message.content_size for message in honza_messages)

        content = (
            f"📊 Milý Danieli, dne {yesterday:%-d.%-m.%Y} jsi veřejně napsal {daniel_content_size} písmenek včetně mezer."
            f"\nBylo to v {len(daniel_messages)} zprávách, v {len(daniel_channels)} různých veřejných kanálech ({len(daniel_threads)}, pokud rozlišuji vlákna)."
            f"\nTo je jako {daniel_content_size / 1800:.1f} normostran."
            f"\nCelkem vidím {daniel_all_content_size} písmenek včetně mezer."
            f"\nBylo to v {len(daniel_all_messages)} zprávách, v {len(daniel_all_channels)} různých kanálech ({len(daniel_all_threads)}, pokud rozlišuji vlákna)."
            f"\nTo je jako {daniel_all_content_size / 1800:.1f} normostran."
            "\nPamatuj však, že nevidím všechno, takže ta celková čísla mohou být výšší."
            f"\nHonza tentýž den veřejně napsal {honza_content_size} písmenek, ale nikdy se to nedoví, protože tyhle zprávy posílám jen tobě."
            f"\n**{czech_weekday}** :abc: {daniel_all_content_size} :speech_left: {len(daniel_all_messages)} <:discordthread:993580255287705681> {len(daniel_all_threads)}"
        )
        logger.info(f"Sending:\n{content}")
        with mutating_discord(channel) as proxy:
            await proxy.send(content=content)
    else:
        logger.info("Last message is recent enough, skipping")
