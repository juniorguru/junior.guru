import asyncio
import random
from datetime import datetime, timedelta

from discord import MessageType

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import (ClubChannelID, ClubMemberID, add_members,
                                         add_reactions, get_missing_reactions, mutating)
from juniorguru.lib.mutations import MutationsNotAllowedError
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage


WELCOME_REACTIONS = ['👋', '🐣', '👍']

WELCOME_BACK_REACTIONS = ['👋', '🔄']

NUMBERS_REACTIONS = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

PROCESS_HISTORY_SINCE = timedelta(days=30)

THREADS_STARTING_AT = datetime(2022, 7, 17, 0, 0)

GREETERS_ROLE = 1062755787153358879

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
    discord_sync.run(discord_task)


@db.connection_context()
async def discord_task(client):
    messages = ClubMessage.channel_listing_since(ClubChannelID.INTRO, datetime.utcnow() - PROCESS_HISTORY_SINCE)
    discord_channel = await client.club_guild.fetch_channel(ClubChannelID.INTRO)
    await asyncio.gather(*[process_message(client, discord_channel, message) for message in messages])

    logger.info('Purging system messages about created threads')
    with mutating(discord_channel) as proxy:
        await proxy.purge(check=is_thread_created, limit=PURGE_SAFETY_LIMIT, after=THREADS_STARTING_AT)


async def process_message(client, discord_channel, message):
    greeters_role = [role for role in client.club_guild.roles if role.id == GREETERS_ROLE][0]
    greeters = greeters_role.members
    greeters_ids = [member.id for member in greeters] + [ClubMemberID.BOT]

    if message.type == 'default' and message.author.id not in greeters_ids and message.is_intro:
        await welcome(discord_channel, message, greeters)
    elif message.type == 'new_member' and message.author.first_seen_on() < message.created_at.date():
        await welcome_back(discord_channel, message)


async def welcome(discord_channel, message, greeters):
    logger_m = logger[f'messages.{message.id}']
    logger_m.info(f'Member #{message.author.id} has an intro message')
    logger_m.debug(f"Welcoming '{message.author.display_name}' with emojis")
    discord_message = await discord_channel.fetch_message(message.id)
    missing_emojis = get_missing_reactions(discord_message.reactions, WELCOME_REACTIONS)
    await add_reactions(discord_message, missing_emojis)

    if message.created_at >= THREADS_STARTING_AT:
        logger_m.debug(f"Ensuring thread for '{message.author.display_name}'")
        thread_name = f'Ahoj {message.author.display_name}!'
        if discord_message.flags.has_thread:
            logger_m.debug(f"Thread for '{message.author.display_name}' already exists")
            thread = await discord_message.guild.fetch_channel(message.id)
        else:
            logger_m.debug(f"Creating thread for '{message.author.display_name}'")
            try:
                with mutating(discord_message, raises=True) as proxy:
                    thread = await proxy.create_thread(name=thread_name)
            except MutationsNotAllowedError:
                logger_m.debug("Skipping, couldn't create the thread")
                return

        if thread.archived or thread.locked:
            logger_m.debug("Skipping the thread, because it's archived or locked")
            return
        if thread.name != thread_name:
            logger_m.debug(f"Renaming thread for '{message.author.display_name}' from '{thread.name}' to '{thread_name}'")
            try:
                with mutating(thread, raises=True) as proxy:
                    thread = await proxy.edit(name=thread_name)
            except MutationsNotAllowedError:
                logger_m.debug("Skipping, couldn't edit the thread")
                return

        discord_messages = [discord_message async for discord_message in thread.history(limit=None)]
        logger_m.debug(f"Ensuring welcome message for '{message.author.display_name}'")
        content_prefix = random.choice(WELCOME_MESSAGE_PREFIXES)
        content = (f'{content_prefix} '
                    'Dík, že se představuješ ostatním, protože to fakt hodně pomáhá v tom, aby šlo pochopit tvou konkrétní situaci. '
                    'Takhle ti můžeme dávat rady na míru, a ne jenom nějaká obecná doporučení <:meowthumbsup:842730599906279494>\n\n'
                    'Potřebuješ pošťouchnout s kariérním rozhodnutím? Pojď to probrat do <#788826407412170752>. '
                    'Vybíráš kurz? Napiš do <#1075052469303906335>. Hledáš konkrétní recenze? Zkus vyhledávání. '
                    'Něco jiného? <#769966887055392768> snese cokoliv 💬\n\n'
                    'Na https://junior.guru/handbook/ najdeš příručku s radami pro všechny, '
                    'kdo se chtějí naučit programovat a najít si práci v oboru. Hodně věcí je už zodpovězeno v ní, tak si ji nezapomeň projít 📖\n\n'
                    'Příručka začíná popisem **osvědčené cesty juniora**, která má **10 fází** 🥚 🐣 🐥 '
                    'Jaké z těch fází se tě zrovna teď týkají? Zaklikni čísla pod touto zprávou ⬇️')
        logger_m.debug(f"Welcome message content: {content!r}")
        try:
            welcome_discord_message = list(filter(is_welcome_message, discord_messages))[0]
            logger_m.debug(f"Welcome message already exists, updating: #{welcome_discord_message.id}")
            if welcome_discord_message.embeds or welcome_discord_message.content != content:
                with mutating(welcome_discord_message) as proxy:
                    await proxy.edit(content=content, suppress=True)
        except IndexError:
            logger_m.debug("Sending welcome message")
            with mutating(thread) as proxy:
                welcome_discord_message = await proxy.send(content=content, suppress=True)

            logger_m.debug("Adding numbers reactions under the welcome message")
            await add_reactions(welcome_discord_message, NUMBERS_REACTIONS, ordered=True)

            logger_m.debug("Analyzing if all greeters are involved")
            thread_members_ids = [member.id for member in (thread.members or await thread.fetch_members())]
            members_to_add = [greeter for greeter in greeters
                            if greeter.id not in thread_members_ids]
            logger_m.debug(f"Found {len(members_to_add)} greeters to add")
            if members_to_add:
                await add_members(thread, members_to_add)


async def welcome_back(discord_channel, message):
    logger_m = logger[f'messages.{message.id}']
    logger_m.info(f'Member #{message.author.id} has returned')
    logger_m.debug(f"Welcoming back '{message.author.display_name}' with emojis")
    discord_message = await discord_channel.fetch_message(message.id)
    missing_emojis = get_missing_reactions(discord_message.reactions, WELCOME_BACK_REACTIONS)
    await add_reactions(discord_message, missing_emojis)


def is_thread_created(discord_message):
    return discord_message.type == MessageType.thread_created


def is_welcome_message(discord_message):
    return discord_message.type == MessageType.default and discord_message.author.id == ClubMemberID.BOT
