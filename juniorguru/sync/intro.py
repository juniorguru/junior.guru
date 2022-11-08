import asyncio
import random
from datetime import datetime, timedelta

from discord import MessageType
from discord.errors import Forbidden

from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, INTRO_CHANNEL,
                                 JUNIORGURU_BOT, MODERATORS_ROLE, run_discord_task)
from juniorguru.cli.sync import main as cli
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage


WELCOME_REACTIONS = ['👋', '🐣', '👍']

WELCOME_BACK_REACTIONS = ['👋', '🔄']

NUMBERS_REACTIONS = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

PROCESS_HISTORY_SINCE = timedelta(days=30)

THREADS_STARTING_AT = datetime(2022, 7, 17, 0, 0)

PURGE_SAFETY_LIMIT = 20

WELCOME_MESSAGE_PREFIXES = [
    'Vítej!',
    'Vítej v klubu!',
    'Vítám tě v klubu!',
    'Vítám tě mezi námi!',
    'Vítej mezi námi!',
    'Čau!',
    'Čáááu!',
    'Ahoj!',
    'Ahój!',
    'Nazdar!',
    'Nazdááár!',
]

ERROR_CODE_THREAD_ARCHIVED = 50083


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['club-content'])
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


async def process_message(client, channel, message):
    moderators_role = [role for role in client.juniorguru_guild.roles if role.id == MODERATORS_ROLE][0]
    moderators = moderators_role.members
    moderators_ids = [member.id for member in moderators] + [JUNIORGURU_BOT]

    if message.type == 'default' and message.author.id not in moderators_ids and message.is_intro:
        await welcome(channel, message, moderators)
    elif message.type == 'new_member' and message.author.first_seen_on() < message.created_at.date():
        await welcome_back(channel, message)


async def welcome(channel, message, moderators):
    logger_m = logger[f'messages.{message.id}']
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
            thread_name = f'Ahoj {message.author.display_name}!'
            if discord_message.flags.has_thread:
                logger_m.debug(f"Thread for '{message.author.display_name}' already exists")
                thread = await discord_message.guild.fetch_channel(message.id)
            else:
                logger_m.debug(f"Creating thread for '{message.author.display_name}'")
                thread = await discord_message.create_thread(name=thread_name)

            if thread.archived or thread.locked:
                logger_m.debug("Skipping the thread, because it's archived or locked")
                return
            if thread.name != thread_name:
                logger_m.debug(f"Renaming thread for '{message.author.display_name}' from '{thread.name}' to '{thread_name}'")
                thread = await thread.edit(name=thread_name)

            discord_messages = [discord_message async for discord_message in thread.history(limit=None)]
            logger_m.debug(f"Ensuring welcome message for '{message.author.display_name}'")
            content_prefix = random.choice(WELCOME_MESSAGE_PREFIXES)
            content = (f'{content_prefix} '
                       'Dík, že se představuješ ostatním, protože to fakt hodně pomáhá v tom, aby šlo pochopit tvou konkrétní situaci. '
                       'Takhle ti můžeme dávat rady na míru, a ne jenom nějaká obecná doporučení <:meowthumbsup:842730599906279494>\n\n'
                       'Potřebuješ pošťouchnout s kariérním rozhodnutím? Pojď to probrat do <#788826407412170752>. '
                       'Vybíráš kurz? Napiš do <#789092262965280778>. Hledáš konkrétní recenze? Zkus vyhledávání. '
                       'Něco jiného? <#769966887055392768> snese cokoliv 💬\n\n'
                       'Na https://junior.guru/handbook/ najdeš příručku s radami pro všechny, '
                       'kdo se chtějí naučit programovat a najít si práci v oboru. Hodně věcí je už zodpovězeno v ní, tak si ji nezapomeň projít 📖\n\n'
                       'Příručka začíná popisem **osvědčené cesty juniora**, která má **10 fází** 🥚 🐣 🐥 '
                       'Jaké z těch fází se tě zrovna teď týkají? Použij reakce s číslama ⬇️')
            logger_m.debug(f"Welcome message content: {content!r}")
            try:
                welcome_discord_message = list(filter(is_welcome_message, discord_messages))[0]
                logger_m.debug(f"Welcome message already exists, updating: #{welcome_discord_message.id}")
                if welcome_discord_message.embeds or welcome_discord_message.content != content:
                    await welcome_discord_message.edit(content=content, suppress=True)
            except IndexError:
                logger_m.debug("Sending welcome message")
                welcome_discord_message = await thread.send(content=content)
                await welcome_discord_message.edit(suppress=True)

            logger_m.debug("Ensuring numbers reactions under the welcome message")
            if get_missing_reactions(welcome_discord_message.reactions, NUMBERS_REACTIONS):
                await welcome_discord_message.clear_reactions()
            await add_reactions(welcome_discord_message, NUMBERS_REACTIONS, ordered=True)

            logger_m.debug("Analyzing if all moderators are involved")
            thread_members_ids = [member.id for member in (thread.members or await thread.fetch_members())]
            members_to_add = [moderator for moderator in moderators
                              if moderator.id not in thread_members_ids]
            logger_m.debug(f"Found {len(members_to_add)} moderators to add")
            if members_to_add:
                await asyncio.gather(*[thread.add_user(member) for member in members_to_add])
        else:
            logger_m.warning('Discord mutations not enabled')


async def welcome_back(channel, message):
    logger_m = logger[f'messages.{message.id}']
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


async def add_reactions(discord_message, emojis, ordered=False):
    logger.debug(f"Reacting to message #{discord_message.id} with emojis: {list(emojis)!r}")
    if not emojis:
        return
    try:
        if ordered:
            for emoji in emojis:
                await discord_message.add_reaction(emoji)
        else:
            await asyncio.gather(*[discord_message.add_reaction(emoji) for emoji in emojis])
    except Forbidden as e:
        if 'maximum number of reactions reached' in str(e).lower():
            logger.warning(f"Message #{discord_message.id} reached maximum number of reactions!")
        else:
            raise e


def is_thread_created(discord_message):
    return discord_message.type == MessageType.thread_created


def is_welcome_message(discord_message):
    return discord_message.type == MessageType.default and discord_message.author.id == JUNIORGURU_BOT
