from datetime import date, timedelta

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import ClubMember, is_message_older_than, mutating
from juniorguru.lib.mutations import MutationsNotAllowed
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.lib.mutations import mutations


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['club-content'])
def main():
    discord_sync.run(discord_task)


@db.connection_context()
async def discord_task(client):
    member = await client.club_guild.fetch_member(ClubMember.DANIEL)
    if member.dm_channel:
        channel = member.dm_channel
    else:
        logger.debug(f"Creating DM channel for {member.display_name} #{member.id}")
        with mutating(member) as proxy:
            channel = await proxy.create_dm()
    if channel is mutations.MutationsNotAllowed:
        logger.warning("Couldn't get the DM channel")
        return

    last_message = None
    async for message in channel.history(limit=None, after=None):
        if message.content.startswith('📊'):
            last_message = message
            break

    yesterday = date.today() - timedelta(days=1)
    if is_message_older_than(last_message, yesterday):
        messages = ClubMessage.select()
        messages = [message for message in messages
                    if message.created_at.date() == yesterday]
        daniel_messages = [message for message in messages if message.author.id == ClubMember.DANIEL]
        daniel_channels = set(message.parent_channel_id for message in daniel_messages)
        daniel_threads = set(message.channel_id for message in daniel_messages)
        daniel_content_size = sum(message.content_size for message in daniel_messages)
        honza_messages = [message for message in messages if message.author.id == ClubMember.HONZA]
        honza_content_size = sum(message.content_size for message in honza_messages)

        content = (
            f"📊 Milý Danieli, dne {yesterday:%A %-d.%-m.%Y} jsi napsal {daniel_content_size} písmenek včetně mezer. "
            f"Bylo to v {len(daniel_messages)} zprávách, v {len(daniel_channels)} různých kanálech ({len(daniel_threads)}, pokud rozlišuji vlákna). "
            f"To je jako {daniel_content_size / 1800:.1f} normostran."
            f"Honza tentýž den napsal {honza_content_size} písmenek, ale nikdy se to nedoví, protože tyhle zprávy posílám jen tobě. "
            f"\n:abc: {daniel_content_size} :speech_left: {len(daniel_messages)} <:discordthread:993580255287705681> {len(daniel_threads)} "
        )
        logger.debug(f'Sending: {content}')
        with mutating(channel) as proxy:
            await proxy.send(content=content)
