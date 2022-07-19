import asyncio
from datetime import datetime, timedelta

from discord import MessageType
from discord.errors import Forbidden

from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED, run_discord_task, INTRO_CHANNEL, JUNIORGURU_BOT, MODERATORS_ROLE
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.sync.club_content import main as club_content_task


WELCOME_REACTIONS = ['👋', '🐣', '👍']

WELCOME_BACK_REACTIONS = ['👋', '🔄']

PROCESS_HISTORY_SINCE = timedelta(days=30)

THREADS_STARTING_AT = datetime(2022, 7, 17, 0, 0)

PURGE_SAFETY_LIMIT = 20


logger = loggers.get(__name__)


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.intro.discord_task')


@db.connection_context()
async def discord_task(client):
    channel = client.juniorguru_guild.system_channel

    if channel.id != INTRO_CHANNEL:
        raise RuntimeError('It is expected that the system channel is the same as the intro channel')

    messages = ClubMessage.channel_listing_since(channel.id, datetime.utcnow() - PROCESS_HISTORY_SINCE)
    await asyncio.gather(*[process_message(client, channel, message) for message in messages])

    logger.info('Purging system messages about created threads')
    if DISCORD_MUTATIONS_ENABLED:
        await channel.purge(check=is_thread_created, limit=PURGE_SAFETY_LIMIT, after=THREADS_STARTING_AT)
    else:
        logger.warning('Discord mutations not enabled')


def is_thread_created(discord_message):
    return discord_message.type == MessageType.thread_created


async def process_message(client, channel, message):
    logger_m = logger.getChild(f'messages.{message.id}')

    moderators_role = [role for role in client.juniorguru_guild.roles if role.id == MODERATORS_ROLE][0]
    moderators_ids = [member.id for member in moderators_role.members] + [JUNIORGURU_BOT]

    if message.type == 'default' and message.author.id not in moderators_ids and message.is_intro:
        logger_m.info(f'Member #{message.author.id} has an intro message')
        logger_m.debug(f"Welcoming '{message.author.display_name}' with emojis")
        discord_message = await channel.fetch_message(message.id)
        missing_emojis = get_missing_reactions(discord_message.reactions, WELCOME_REACTIONS)
        if DISCORD_MUTATIONS_ENABLED:
            await add_reactions(discord_message, missing_emojis)
        else:
            logger_m.warning('Discord mutations not enabled')

        if message.created_at >= THREADS_STARTING_AT:
            logger_m.debug(f"Ensuring thread for '{message.author.display_name}'")
            if DISCORD_MUTATIONS_ENABLED:
                if discord_message.flags.has_thread:
                    logger_m.debug(f"Thread for '{message.author.display_name}' already exists")
                    thread = await discord_message.guild.fetch_channel(message.id)
                else:
                    logger_m.debug(f"Creating thread for '{message.author.display_name}'")
                    thread = await discord_message.create_thread(name=f'Ahoj {message.author.display_name}!')
                message.author.intro_thread_id = thread.id
                message.author.save()
            else:
                logger_m.warning('Discord mutations not enabled')

    elif message.type == 'new_member' and message.author.first_seen_on() < message.created_at.date():
        logger_m.info(f'Member #{message.author.id} has returned')
        logger_m.debug(f"Welcoming back '{message.author.display_name}' with emojis")
        discord_message = await channel.fetch_message(message.id)
        missing_emojis = get_missing_reactions(discord_message.reactions, WELCOME_BACK_REACTIONS)
        if DISCORD_MUTATIONS_ENABLED:
            await add_reactions(discord_message, missing_emojis)
        else:
            logger_m.warning('Discord mutations not enabled')


def get_missing_reactions(existing_reactions, ensure_emojis):
    return set(ensure_emojis) - {reaction.emoji for reaction in existing_reactions if reaction.me}


async def add_reactions(discord_message, emojis):
    logger.debug(f"Reacting to message #{discord_message.id} with emojis: {emojis!r}")
    if not emojis:
        return
    try:
        await asyncio.gather(*[discord_message.add_reaction(emoji) for emoji in emojis])
    except Forbidden as e:
        if 'maximum number of reactions reached' in str(e).lower():
            logger.warning(f"Message #{discord_message.id} reached maximum number of reactions!")
        else:
            raise e
