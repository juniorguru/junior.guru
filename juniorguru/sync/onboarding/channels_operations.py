from datetime import date, timedelta

import discord
from slugify import slugify

from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, JUNIORGURU_BOT,
                                 MODERATORS_ROLE)
from juniorguru.models.club import ClubMessage
from juniorguru.sync.onboarding.categories import manage_categories


TODAY = date.today()

CHANNELS_OPERATIONS = {}

CHANNEL_DELETE_TIMEOUT = timedelta(days=30)


logger = loggers.get(__name__)


def channels_operation(operation_name):
    def decorator(operation):
        CHANNELS_OPERATIONS[operation_name] = operation
    return decorator


@channels_operation('update')
@manage_categories
async def update_onboarding_channel(client, member, channel, category):
    logger_c = logger.getChild(f'channels.{channel.id}')
    logger_c.info(f"Updating (member #{member.id})")
    if category and category.id != channel.category.id:
        logger_c.debug(f"Moving from category #{channel.category.id} to #{category.id}")
    channel_data = await prepare_onboarding_channel_data(client, category, member)
    if DISCORD_MUTATIONS_ENABLED:
        await channel.edit(**channel_data)
    else:
        logger_c.warning('Discord mutations not enabled')
    member.onboarding_channel_id = channel.id
    member.save()


@channels_operation('create')
@manage_categories
async def create_onboarding_channel(client, member, category):
    logger_c = logger.getChild('channels')
    logger_c.info(f"Creating (member #{member.id})")
    channel_data = await prepare_onboarding_channel_data(client, category, member)
    if DISCORD_MUTATIONS_ENABLED:
        channel = await client.juniorguru_guild.create_text_channel(**channel_data)
        member.onboarding_channel_id = channel.id
        member.save()
    else:
        logger_c.warning('Discord mutations not enabled')


@channels_operation('delete')
async def delete_onboarding_channel(client, channel):
    logger_c = logger.getChild(f'channels.{channel.id}')
    logger_c.info("Deleting")
    if DISCORD_MUTATIONS_ENABLED:
        await channel.delete()
    else:
        logger_c.warning('Discord mutations not enabled')


@channels_operation('close')
async def close_onboarding_channel(client, channel):
    logger_c = logger.getChild(f'channels.{channel.id}')
    logger_c.info("Closing")
    last_message_on = ClubMessage.last_message(channel.id).created_at.date()
    current_period = TODAY - last_message_on
    if current_period < CHANNEL_DELETE_TIMEOUT:
        logger_c.warning(f"Would delete, but waiting: Last message {last_message_on}, currently {current_period.days} days, timeout {CHANNEL_DELETE_TIMEOUT.days} days")
    elif DISCORD_MUTATIONS_ENABLED:
        await channel.delete()
    else:
        logger_c.warning('Discord mutations not enabled')


async def prepare_onboarding_channel_data(client, category, member):
    name = f'{slugify(member.display_name, allow_unicode=True)}-tipy'
    topic = f'Soukromý kanál s tipy jen pro tebe! 🦸 {member.display_name} #{member.id}'
    if not category:
        raise ValueError('No category provided')
    moderators_role = [role for role in client.juniorguru_guild.roles if role.id == MODERATORS_ROLE][0]
    overwrites = {
        client.juniorguru_guild.default_role: discord.PermissionOverwrite(read_messages=False),
        (await client.get_or_fetch_user(JUNIORGURU_BOT)): discord.PermissionOverwrite(read_messages=True),
        moderators_role: discord.PermissionOverwrite(read_messages=True),
        (await client.get_or_fetch_user(member.id)): discord.PermissionOverwrite(read_messages=True),
    }
    return dict(name=name, topic=topic, category=category, overwrites=overwrites)
