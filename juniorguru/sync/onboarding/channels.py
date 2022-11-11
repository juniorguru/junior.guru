import asyncio
import re
from datetime import date

from juniorguru.lib import loggers
from juniorguru.lib.asyncio_extra import chunks
from juniorguru.lib.club import ANNOUNCEMENTS_CHANNEL
from juniorguru.models.club import ClubUser
from juniorguru.sync.onboarding.categories import (create_enough_categories,
                                                   delete_empty_categories,
                                                   is_onboarding_category)
from juniorguru.sync.onboarding.channels_operations import CHANNELS_OPERATIONS


CHANNEL_TOPIC_RE = re.compile(r'\#(?P<id>\d+)\s*$')

CHANNELS_OPERATIONS_CHUNK_SIZE = 10

BETA_USERS_MESSAGE = 1014611670598942743

BETA_USERS_EMOJI = '🐇'

BETA_USERS_DATE = date(2022, 7, 17)


logger = loggers.from_path(__file__)


async def manage_channels(client):
    beta_users_ids = await fetch_beta_users(client)
    logger.info(f'Found {len(beta_users_ids)} BETA volunteers')

    members = [member for member in ClubUser.members_listing()
               if member.id in beta_users_ids or member.first_seen_on() > BETA_USERS_DATE]
    logger.info(f'Onboarding {len(members)} members')

    channels = list(filter(is_onboarding_channel, client.juniorguru_guild.channels))
    logger.info(f"Managing {len(channels)} existing onboarding channels")
    await create_enough_categories(client, len(members) + len(channels))
    channels_operations = prepare_channels_operations(channels, members)
    await execute_channels_operations(client, channels_operations)
    await delete_empty_categories(client)


async def fetch_beta_users(client):
    announcements_channel = await client.juniorguru_guild.fetch_channel(ANNOUNCEMENTS_CHANNEL)
    beta_users_message = await announcements_channel.fetch_message(BETA_USERS_MESSAGE)
    beta_users_reaction = [reaction for reaction
                           in beta_users_message.reactions
                           if reaction.emoji == BETA_USERS_EMOJI][0]
    return [beta_user.id async for beta_user
            in beta_users_reaction.users()]


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


async def execute_channels_operations(client, operations):
    channels_operations_chunks = chunks(operations,
                                        size=CHANNELS_OPERATIONS_CHUNK_SIZE)
    for n, channels_operations_chunk in enumerate(channels_operations_chunks, start=1):
        logger.debug(f'Processing chunk #{n} of {len(channels_operations_chunk)} channels operations')
        await asyncio.gather(*[
            CHANNELS_OPERATIONS[operation_name](client, *operation_payload)
            for operation_name, operation_payload in channels_operations_chunk
        ])


def parse_member_id(channel_topic):  # once I write tests, test for None input, too
    try:
        match = CHANNEL_TOPIC_RE.search(channel_topic)
        return int(match.groupdict()['id'])
    except (AttributeError, KeyError, TypeError):
        raise ValueError("Given channel topic doesn't contain reference to a member ID")


def is_onboarding_channel(channel):
    return channel.category and is_onboarding_category(channel.category)
