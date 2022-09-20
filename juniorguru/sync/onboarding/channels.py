import re
import itertools
import math
import asyncio
from datetime import timedelta, date
from operator import attrgetter

import discord
from slugify import slugify

from juniorguru.lib.asyncio_extra import chunks
from juniorguru.lib import loggers
from juniorguru.lib.club import JUNIORGURU_BOT, DISCORD_MUTATIONS_ENABLED, MODERATORS_ROLE, ANNOUNCEMENTS_CHANNEL
from juniorguru.models.club import ClubUser, ClubMessage


TODAY = date.today()

ONBOARDING_CATEGORY_NAME = '👋 Tipy pro tebe'

CHANNEL_TOPIC_RE = re.compile(r'\#(?P<id>\d+)\s*$')

CHANNEL_DELETE_TIMEOUT = timedelta(days=30)

CHANNELS_OPERATIONS_CHUNK_SIZE = 10

CHANNELS_PER_CATEGORY_LIMIT = 50

ONBOARDING_CHANNELS_LIMIT = 100

CHANNELS_OPERATIONS = {}

BETA_USERS_MESSAGE = 1014611670598942743

BETA_USERS_DATE = date(2022, 7, 17)


logger = loggers.get(__name__)


async def manage_channels(client):
    logger.info('Figuring out BETA users')
    announcements_channel = await client.juniorguru_guild.fetch_channel(ANNOUNCEMENTS_CHANNEL)
    beta_users_message = await announcements_channel.fetch_message(BETA_USERS_MESSAGE)
    beta_users_reaction = [reaction for reaction in beta_users_message.reactions if reaction.emoji == '🐇'][0]
    beta_users_ids = [beta_user.id async for beta_user in beta_users_reaction.users()]
    logger.info(f'Found {len(beta_users_ids)} BETA users who volunteered')

    members = [member for member in ClubUser.members_listing()
               if member.id in beta_users_ids or member.first_seen_on() > BETA_USERS_DATE]
    if len(members) > ONBOARDING_CHANNELS_LIMIT:
        raise RuntimeError(f"Need to onboard {len(members)} members, but the limit is {ONBOARDING_CHANNELS_LIMIT}")
    logger.info(f'Onboarding {len(members)} members')

    categories_count = math.ceil(len(members) / CHANNELS_PER_CATEGORY_LIMIT)
    categories = [category for category in client.juniorguru_guild.categories
                  if category.name == ONBOARDING_CATEGORY_NAME]
    if len(categories) < categories_count:
        logger.info(f"Need {categories_count} categories, but found only {len(categories)}")
        categories_count_to_add = categories_count - len(categories)
        for i in range(categories_count_to_add):
            logger.debug(f"Adding onboarding category #{len(categories) + i + 1}")
            position = max([category.position for category in categories])
            if DISCORD_MUTATIONS_ENABLED:
                categories.append(await client.juniorguru_guild.create_category_channel(ONBOARDING_CATEGORY_NAME, position=position))
            else:
                logger.warning('Discord mutations not enabled')

    channels = list(itertools.chain.from_iterable(category.channels for category in categories))
    logger.info(f"Managing {len(channels)} existing onboarding channels")
    channels_operations = prepare_channels_operations(channels, members)
    await execute_channels_operations(client, categories, channels_operations)

    for category in categories:
        if len(category.channels) == 0:
            logger.debug("Found onboarding category with zero channels, deleting")
            if DISCORD_MUTATIONS_ENABLED:
                await category.delete()
            else:
                logger.warning('Discord mutations not enabled')


async def execute_channels_operations(client, categories, operations):
    channels_operations_chunks = chunks(operations,
                                       size=CHANNELS_OPERATIONS_CHUNK_SIZE)
    for n, channels_operations_chunk in enumerate(channels_operations_chunks, start=1):
        logger.debug(f'Processing chunk #{n} of {len(channels_operations_chunk)} channels operations')
        await asyncio.gather(*[
            get_channels_operation_function(operation_name)(client, categories, *operation_payload)
            for operation_name, operation_payload in channels_operations_chunk
        ])


def prepare_channels_operations(channels, members):
    members_channels_mapping = {}
    operations = []

    for channel in channels:
        try:
            member_id = parse_member_id(channel.topic)
        except ValueError:
            operations.append(('delete', (channel,)))
        else:
            members_channels_mapping[member_id] = channel

    for member in members:
        try:
            channel = members_channels_mapping.pop(member.id)
            operations.append(('update', (member, channel)))
        except KeyError:
            operations.append(('create', (member,)))

    for channel in members_channels_mapping.values():
        operations.append(('close', (channel,)))

    return operations


def parse_member_id(channel_topic):
    match = CHANNEL_TOPIC_RE.search(channel_topic)
    try:
        return int(match.groupdict()['id'])
    except (AttributeError, KeyError, TypeError):
        raise ValueError("Given channel topic doesn't contain reference to a member ID")


async def prepare_onboarding_channel_data(client, category, member):
    name = f'{slugify(member.display_name, allow_unicode=True)}-tipy'
    topic = f'Soukromý kanál s tipy jen pro tebe! 🦸 {member.display_name} #{member.id}'
    overwrites = {
        client.juniorguru_guild.default_role: discord.PermissionOverwrite(read_messages=False),
        (await client.get_or_fetch_user(JUNIORGURU_BOT)): discord.PermissionOverwrite(read_messages=True),
        get_role(client.juniorguru_guild, MODERATORS_ROLE): discord.PermissionOverwrite(read_messages=True),
        (await client.get_or_fetch_user(member.id)): discord.PermissionOverwrite(read_messages=True),
    }
    return dict(name=name, topic=topic, category=category, overwrites=overwrites)


def get_available_category(categories):
    available_categories = [category for category in categories
                            if len(category.channels) < CHANNELS_PER_CATEGORY_LIMIT]
    return sorted(available_categories, key=attrgetter('position'))[0]


def get_channels_operation_function(name):
    return globals()[f'{name}_onboarding_channel']


def get_role(guild, id):
    return [role for role in guild.roles if role.id == id][0]


def channels_operation(operation_name):
    def decorator(operation):
        CHANNELS_OPERATIONS[operation_name] = operation
    return decorator


@channels_operation('update')
async def update_onboarding_channel(client, categories, member, channel):
    logger_c = logger.getChild(f'channels.{channel.id}')
    logger_c.info(f"Updating (member #{member.id})")
    category = get_available_category(categories)
    if channel.category.id != category.id:
        logger_c.debug(f"Moving from category #{channel.category.id} to #{category.id}")
    channel_data = await prepare_onboarding_channel_data(client, category, member)
    if DISCORD_MUTATIONS_ENABLED:
        await channel.edit(**channel_data)
    else:
        logger_c.warning('Discord mutations not enabled')
    member.onboarding_channel_id = channel.id
    member.save()


@channels_operation('create')
async def create_onboarding_channel(client, categories, member):
    logger_c = logger.getChild('channels')
    logger_c.info(f"Creating (member #{member.id})")
    category = get_available_category(categories)
    channel_data = await prepare_onboarding_channel_data(client, category, member)
    if DISCORD_MUTATIONS_ENABLED:
        channel = await client.juniorguru_guild.create_text_channel(**channel_data)
        member.onboarding_channel_id = channel.id
        member.save()
    else:
        logger_c.warning('Discord mutations not enabled')


@channels_operation('delete')
async def delete_onboarding_channel(client, categories, channel):
    logger_c = logger.getChild(f'channels.{channel.id}')
    logger_c.info("Deleting")
    if DISCORD_MUTATIONS_ENABLED:
        await channel.delete()
    else:
        logger_c.warning('Discord mutations not enabled')


@channels_operation('close')
async def close_onboarding_channel(client, categories, channel):
    logger_c = logger.getChild(f'channels.{channel.id}')
    logger_c.info("Closing")
    last_message_on = ClubMessage.last_message(channel.id).created_at.date()
    threshold_on = (TODAY - CHANNEL_DELETE_TIMEOUT)
    if last_message_on > threshold_on:
        logger_c.warning(f"Would delete, but waiting (last message on {last_message_on} > threshold on {threshold_on}, timeout is {CHANNEL_DELETE_TIMEOUT})")
    elif DISCORD_MUTATIONS_ENABLED:
        await channel.delete()
    else:
        logger_c.warning('Discord mutations not enabled')
