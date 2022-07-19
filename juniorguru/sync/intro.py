import asyncio
from datetime import datetime, timedelta

from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED, run_discord_task, INTRO_CHANNEL, JUNIORGURU_BOT, MODERATORS_ROLE
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.sync.club_content import main as club_content_task


WELCOME_REACTIONS = ['👋', '🐣', '👍']

WELCOME_BACK_REACTIONS = ['👋', '🔄']


logger = loggers.get(__name__)


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

    moderators_role = [role for role in client.juniorguru_guild.roles if role.id == MODERATORS_ROLE][0]
    moderators_ids = [member.id for member in moderators_role.members] + [JUNIORGURU_BOT]

    # TODO
    # if message.created_at < (datetime.now() - timedelta(days=5)):
    #     return

    if message.type == 'default' and message.author.id not in moderators_ids and message.is_intro:
        logger_m.info(f'Member #{message.author.id} has an intro message')
        logger_m.debug(f"Welcoming '{message.author.display_name}' with emojis")
        discord_message = await channel.fetch_message(message.id)
        missing_emojis = get_missing_reactions(discord_message.reactions, WELCOME_REACTIONS)
        if missing_emojis:
            logger_m.debug(f"Missing emojis: {missing_emojis}")
            if DISCORD_MUTATIONS_ENABLED:
                await asyncio.gather(*[discord_message.add_reaction(emoji) for emoji in missing_emojis])
            else:
                logger.warning('Discord mutations not enabled')

        # logger_m.debug(f"Starting a thread for '{message.author.display_name}'")
        # print(message.thread)
        # thread = await discord_message.create_thread(f'Ahoj {message.author.display_name}!')

    elif message.type == 'new_member' and message.author.first_seen_on() < message.created_at.date():
        logger_m.info(f'Member #{message.author.id} has returned')
        logger_m.debug(f"Welcoming back '{message.author.display_name}' with emojis")
        discord_message = await channel.fetch_message(message.id)
        missing_emojis = get_missing_reactions(discord_message.reactions, WELCOME_BACK_REACTIONS)
        if missing_emojis:
            logger_m.debug(f"Missing emojis: {missing_emojis}")
            if DISCORD_MUTATIONS_ENABLED:
                await asyncio.gather(*[discord_message.add_reaction(emoji) for emoji in missing_emojis])
            else:
                logger.warning('Discord mutations not enabled')


def get_missing_reactions(existing_reactions, ensure_emojis):
    return set(ensure_emojis) - {reaction.emoji for reaction in existing_reactions if reaction.me}
