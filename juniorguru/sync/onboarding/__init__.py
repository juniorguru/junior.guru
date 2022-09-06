import re
import asyncio
import math
from datetime import date, timedelta
import itertools
from operator import attrgetter

import discord
from slugify import slugify

from juniorguru.lib.asyncio_extra import chunks
from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task, JUNIORGURU_BOT, DISCORD_MUTATIONS_ENABLED, MODERATORS_ROLE, ANNOUNCEMENTS_CHANNEL
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubUser, ClubMessage
from juniorguru.sync.club_content import main as club_content_task
from juniorguru.sync.onboarding.scheduled_messages import SCHEDULED_MESSAGES


logger = loggers.get(__name__)


TODAY = date.today()

CHANNEL_TOPIC_RE = re.compile(r'\#(?P<id>\d+)\s*$')

CHANNELS_PER_CATEGORY_LIMIT = 50

ONBOARDING_CHANNELS_LIMIT = 100

ONBOARDING_CATEGORY_NAME = '👋 Tipy pro tebe'

CHANNEL_DELETE_TIMEOUT = timedelta(days=30 * 3)

CHANNELS_OPERATIONS_CHUNK_SIZE = 10

MEMBERS_CHUNK_SIZE = 10

BETA_USERS_MESSAGE = 1014611670598942743

BETA_USERS_DATE = date(2022, 7, 17)

NEXT_TIP_EMOJI = '✅'


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.onboarding.discord_task')


@db.connection_context()
async def discord_task(client):
    await manage_channels(client)
    await send_messages(client)


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


def get_channels_operation_function(name):
    return globals()[f'{name}_onboarding_channel']


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


async def delete_onboarding_channel(client, categories, channel):
    logger_c = logger.getChild(f'channels.{channel.id}')
    logger_c.info("Deleting")
    if DISCORD_MUTATIONS_ENABLED:
        await channel.delete()
    else:
        logger_c.warning('Discord mutations not enabled')


async def close_onboarding_channel(client, categories, channel):
    logger_c = logger.getChild(f'channels.{channel.id}')
    logger_c.info("Closing")
    last_message_on = ClubMessage.last_message(channel.id).created_at.date()
    threshold_on = (TODAY - CHANNEL_DELETE_TIMEOUT)
    if last_message_on > threshold_on:
        logger_c.warning(f"Would delete the channel, but waiting (last message on {last_message_on} > {threshold_on})")
    elif DISCORD_MUTATIONS_ENABLED:
        await channel.delete()
    else:
        logger_c.warning('Discord mutations not enabled')


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


def get_role(guild, id):
    return [role for role in guild.roles if role.id == id][0]


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


async def send_messages(client):
    members_chunks = chunks(ClubUser.onboarding_listing(),
                            size=MEMBERS_CHUNK_SIZE)
    for n, members_chunk in enumerate(members_chunks, start=1):
        logger.debug(f'Processing chunk #{n} of {len(members_chunk)} members')
        await asyncio.gather(*[
            send_messages_to_member(client, member)
            for member in members_chunk
        ])


async def send_messages_to_member(client, member):
    logger_m = logger.getChild(f'members.{member.id}')
    logger_m.debug('Preparing messages')
    messages = prepare_messages(ClubMessage.channel_listing_bot(member.onboarding_channel_id),
                                SCHEDULED_MESSAGES, TODAY, context=dict(member=member))
    if not messages:
        logger_m.debug('Nothing to do')
        return
    logger_m.info(f'Processing {len(messages)} messages')

    channel = await client.fetch_channel(member.onboarding_channel_id)
    for message_id, message_content in messages:
        if message_id:
            logger_m.debug(f'Editing message {message_content[0]}: {len(message_content)} characters')
            if DISCORD_MUTATIONS_ENABLED:
                discord_message = await channel.fetch_message(message_id)
                message_data = await create_message_data(client, member, message_content)
                await discord_message.edit(**message_data)
            else:
                logger_m.warning('Discord mutations not enabled')
        else:
            logger_m.debug(f'Sending message {message_content[0]}: {len(message_content)} characters')
            if DISCORD_MUTATIONS_ENABLED:
                message_data = await create_message_data(client, member, message_content)
                discord_message = await channel.send(**message_data)
                await discord_message.add_reaction(NEXT_TIP_EMOJI)
            else:
                logger_m.warning('Discord mutations not enabled')


async def create_message_data(client, member, content):
    return dict(content=content,
                embed=discord.Embed(colour=discord.Colour.from_rgb(120, 179, 84),
                                    description='Máš přečteno a chceš dostat další tip? Klikni na zaškrtávátko pod zprávou'),
                allowed_mentions=discord.AllowedMentions(everyone=True,
                                                         users=[await client.get_or_fetch_user(member.id)],
                                                         roles=False,
                                                         replied_user=True))


def prepare_messages(history, scheduled_messages, today, context=None):
    messages = []
    past_messages = {message.emoji_prefix: message
                     for message in history
                     if message.emoji_prefix in scheduled_messages}
    context = context or {}

    # append messages to edit
    for emoji_prefix, message in past_messages.items():
        render_content = scheduled_messages[emoji_prefix]
        scheduled_content = prepare_message_content(emoji_prefix, render_content, context)
        if message.content != scheduled_content:
            messages.append((message.id, scheduled_content))

    # don't add a message twice the same day
    if past_messages:
        latest_past_message_on = sorted(past_messages.values(),
                                        key=lambda message: message.created_at,
                                        reverse=True)[0].created_at.date()
        if latest_past_message_on == today:
            return messages

    # append messages to add
    for emoji_prefix, render_content in scheduled_messages.items():
        if emoji_prefix not in past_messages:
            scheduled_content = prepare_message_content(emoji_prefix, render_content, context)
            messages.append((None, scheduled_content))
            break

    return messages


def prepare_message_content(emoji, render_content, context):
    return f'{emoji} {render_content(context).strip()}'
