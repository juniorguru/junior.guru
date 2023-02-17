from datetime import date, timedelta

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, HONZAJAVOREK,
                                 is_message_older_than, run_discord_task)
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage


logger = loggers.from_path(__file__)


DANIELSRB = 652142810291765248


@cli.sync_command(dependencies=['club-content'])
def main():
    run_discord_task('juniorguru.sync.daniel.discord_task')


@db.connection_context()
async def discord_task(client):
    member = await client.juniorguru_guild.fetch_member(DANIELSRB)
    if member.dm_channel:
        channel = member.dm_channel
    else:
        logger.debug(f"Creating DM channel for {member.display_name} #{member.id}")
        channel = await member.create_dm()

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
        daniel_messages = [message for message in messages if message.author.id == DANIELSRB]
        daniel_channels = set(message.parent_channel_id for message in daniel_messages)
        daniel_threads = set(message.channel_id for message in daniel_messages)
        daniel_content_size = sum(message.content_size for message in daniel_messages)
        honza_messages = [message for message in messages if message.author.id == HONZAJAVOREK]
        honza_content_size = sum(message.content_size for message in honza_messages)

        content = (
            f"📊 Milý Danieli, dne {yesterday:%-d.%-m.%Y} jsi napsal {daniel_content_size} písmenek včetně mezer. "
            f"Bylo to v {len(daniel_messages)} zprávách, v {len(daniel_channels)} různých kanálech ({len(daniel_threads)}, pokud rozlišuji vlákna). "
            f"To je jako {daniel_content_size / 1800:.1f} normostran nebo "
            f"{daniel_content_size / 203867:.1f} dokumentů obsahujících kompletní pravidla ragby. "
            f"Honza tentýž den napsal {honza_content_size} písmenek, ale nikdy se to nedoví, protože tyhle zprávy posílám jen tobě. "
        )
        logger.debug(f'Sending: {content}')
        if DISCORD_MUTATIONS_ENABLED:
            await channel.send(content=content)
        else:
            logger.warning('Discord mutations not enabled')
