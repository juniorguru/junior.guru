from datetime import date, timedelta

import discord
from slugify import slugify

from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, JUNIORGURU_BOT)
from juniorguru.models.club import ClubMessage
from juniorguru.sync.onboarding.categories import manage_category


TODAY = date.today()

CHANNELS_OPERATIONS = {}

CHANNEL_DELETE_TIMEOUT = timedelta(days=30)

ONBOARDING_MODERATORS_ROLE = 1062768651188580494


logger = loggers.from_path(__file__)


def channels_operation(operation_name):
    def decorator(operation):
        CHANNELS_OPERATIONS[operation_name] = operation
    return decorator


@channels_operation('update')
async def update_onboarding_channel(client, member, channel):
    logger_c = logger[f'channels.{channel.id}']
    logger_c.info(f"Updating (member #{member.id})")
    channel_data = await prepare_onboarding_channel_data(client, member)
    if DISCORD_MUTATIONS_ENABLED:
        await channel.edit(**channel_data)
    else:
        logger_c.warning('Discord mutations not enabled')
    member.onboarding_channel_id = channel.id
    member.save()


@channels_operation('create')
async def create_onboarding_channel(client, member):
    logger_c = logger['channels']
    logger_c.info(f"Creating (member #{member.id})")
    channel_data = await prepare_onboarding_channel_data(client, member)
    if DISCORD_MUTATIONS_ENABLED:
        async def create_channel(category):
            channel = await client.juniorguru_guild.create_text_channel(category=category, **channel_data)
            member.onboarding_channel_id = channel.id
            member.save()
        await manage_category(client.juniorguru_guild, create_channel)
    else:
        logger_c.warning('Discord mutations not enabled')


@channels_operation('delete')
async def delete_onboarding_channel(client, channel):
    logger_c = logger[f'channels.{channel.id}']
    logger_c.info("Deleting")
    if DISCORD_MUTATIONS_ENABLED:
        await channel.delete()
    else:
        logger_c.warning('Discord mutations not enabled')


@channels_operation('close')
async def close_onboarding_channel(client, channel):
    logger_c = logger[f'channels.{channel.id}']
    logger_c.info("Closing")
    last_message_on = ClubMessage.last_message(channel.id).created_at.date()
    current_period = TODAY - last_message_on
    if current_period < CHANNEL_DELETE_TIMEOUT:
        logger_c.warning(f"Waiting before deleting. Last message {last_message_on}, currently {current_period.days} days, timeout {CHANNEL_DELETE_TIMEOUT.days} days")
    elif DISCORD_MUTATIONS_ENABLED:
        await channel.delete()
    else:
        logger_c.warning('Discord mutations not enabled')


async def prepare_onboarding_channel_data(client, member):
    name = f'{slugify(member.display_name, allow_unicode=True)}-tipy'
    topic = f'Soukromý kanál s tipy jen pro tebe! 🦸 {member.display_name} #{member.id}'
    onboarding_moderators_role = [role for role in client.juniorguru_guild.roles if role.id == ONBOARDING_MODERATORS_ROLE][0]
    overwrites = {
        client.juniorguru_guild.default_role: discord.PermissionOverwrite(read_messages=False),
        (await client.get_or_fetch_user(JUNIORGURU_BOT)): discord.PermissionOverwrite(read_messages=True),
        onboarding_moderators_role: discord.PermissionOverwrite(read_messages=True),
        (await client.get_or_fetch_user(member.id)): discord.PermissionOverwrite(read_messages=True),
    }
    return dict(name=name, topic=topic, overwrites=overwrites)
