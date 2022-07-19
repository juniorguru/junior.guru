import asyncio

from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED, run_discord_task, INTRO_CHANNEL
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.sync.club_content import main as club_content_task


logger = loggers.get(__name__)


MESSAGES_CHUNK_SIZE = 10


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.intro.discord_task')


@db.connection_context()
async def discord_task(client):
    channel = client.juniorguru_guild.system_channel

    if channel.id != INTRO_CHANNEL:
        raise RuntimeError('It is expected that the system channel is the same as the intro channel')

    await asyncio.gather(*[
        process_message(client, channel, message)
        for message in ClubMessage.channel_listing(channel.id)
    ])


async def process_message(client, channel, message):
    logger_m = logger.getChild(f'messages.{message.id}')

    if message.type == 'new_member' and message.author.first_seen_on() < message.created_at.date():
        logger_m.info(f'It looks like member #{message.author.id} has returned')
        discord_message = await channel.fetch_message(message.id)
        missing_emojis = ensure_reactions(discord_message.reactions, ['👋', '🔄'])
        if missing_emojis:
            logger_m.debug(f'Missing emojis: {missing_emojis}')
            if DISCORD_MUTATIONS_ENABLED:
                await asyncio.gather(*[discord_message.add_reaction(emoji) for emoji in missing_emojis])
            else:
                logger.warning('Discord mutations not enabled')


def ensure_reactions(existing_reactions, emojis):
    return set(emojis) - {reaction.emoji for reaction in existing_reactions if reaction.me}
