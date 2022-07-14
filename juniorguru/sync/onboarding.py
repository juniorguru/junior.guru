import re
import asyncio
from datetime import date

import discord
from slugify import slugify

from juniorguru.lib.asyncio_extra import chunks
from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task, JUNIORGURU_BOT, DISCORD_MUTATIONS_ENABLED
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubUser, ClubMessage
from juniorguru.sync.club_content import main as club_content_task


logger = loggers.get(__name__)


CHANNEL_TOPIC_RE = re.compile(r'\#(?P<id>\d+)\s*$')

ONBOARDING_CHANNELS_CATEGORY = 992438896078110751

MODERATORS_ROLE = 795609174385098762

MEMBERS_CHUNK_SIZE = 10

SCHEDULED_MESSAGES = {
    '👋': 'Smrdíme v klubu!',
    '🌯': 'Žereme burrito',
    '💤': 'Spíme',
    '🆗': 'Jsme OK',
    '🟡': 'Hele žluté kolečko',
    '🟥': 'Hele červený čtvereček',
    '🤡': 'Klauni toto!',
}


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.onboarding.manage_channels')
    run_discord_task('juniorguru.sync.onboarding.send_tips')


@db.connection_context()
async def manage_channels(client):
    category = await client.fetch_channel(ONBOARDING_CHANNELS_CATEGORY)
    members_channels_mapping = {}

    for channel in category.channels:
        logger.debug(f"Identifying channel #{channel.name} from its topic: {channel.topic}")
        match = CHANNEL_TOPIC_RE.search(channel.topic)
        try:
            member_id = match.groupdict()['id']
        except (AttributeError, KeyError):
            logger.error(f"Channel #{channel.name} couldn't be identified, removing")
            if DISCORD_MUTATIONS_ENABLED:
                await channel.delete()
            else:
                logger.warning('Discord mutations not enabled')
        else:
            logger.info(f"Channel #{channel.name} identified as onboarding channel for member #{member_id}")
            members_channels_mapping[int(member_id)] = channel

    permissions = {
        client.juniorguru_guild.default_role: discord.PermissionOverwrite(read_messages=False),
        (await client.get_or_fetch_user(JUNIORGURU_BOT)): discord.PermissionOverwrite(read_messages=True),
        get_role(client.juniorguru_guild, MODERATORS_ROLE): discord.PermissionOverwrite(read_messages=True),
    }
    for member in ClubUser.members_listing():
        if member.id != 652142810291765248:  # TODO
            continue

        try:
            channel = members_channels_mapping.pop(member.id)
            logger.info(f"Onboarding channel for member #{member.id} already exists")
        except KeyError:
            logger.info(f"Onboarding channel for member #{member.id} needs to be created")
            overwrites = {
                (await client.get_or_fetch_user(member.id)): discord.PermissionOverwrite(read_messages=True),
                **permissions,
            }
            channel_name = f'{slugify(member.display_name, allow_unicode=True)}-tipy'
            channel_topic = f'Tipy a soukromý kanál jen pro tebe! 🦸 {member.display_name} #{member.id}'
            channel = await client.juniorguru_guild.create_text_channel(name=channel_name,
                                                                        topic=channel_topic,
                                                                        category=category,
                                                                        overwrites=overwrites)
        logger.debug(f"Setting onboarding channel for member #{member.id} to #{channel.id} and saving")
        member.onboarding_channel_id = channel.id
        member.save()

    logger.debug(f'There are {len(members_channels_mapping)} onboarding channels left')
    for member_id, channel in members_channels_mapping.items():
        logger.warning(f"Deleting onboarding channel #{channel.name}, member #{member.id} is gone")
        if DISCORD_MUTATIONS_ENABLED:
            await channel.delete()
        else:
            logger.warning('Discord mutations not enabled')


@db.connection_context()
async def send_tips(client):
    today = date.today()
    members_chunks = chunks(ClubUser.members_listing(),
                            size=MEMBERS_CHUNK_SIZE)
    for n, members_chunk in enumerate(members_chunks, start=1):
        logger.debug(f'Processing chunk #{n} of {len(members_chunk)} members')
        await asyncio.gather(*[
            process_member(client, member, today)
            for member in members_chunk
        ])


async def process_member(client, member, today):
    if member.id != 652142810291765248:  # TODO
        return

    logger_m = logger.getChild(f'members.{member.id}')
    if not member.onboarding_channel_id:
        logger_m.warning('Missing onboarding channel, skipping!')
        return

    logger_m.debug('Preparing messages')
    messages = prepare_messages(ClubMessage.channel_listing_bot(member.onboarding_channel_id),
                                SCHEDULED_MESSAGES, today)
    if not messages:
        logger_m.debug('Nothing to do')
        return
    logger_m.info(f'Processing {len(messages)} messages')

    discord_channel = await client.fetch_channel(member.onboarding_channel_id)
    for message_id, message_content in messages:
        if message_id:
            logger_m.debug(f'Editing message: {message_content}')
            if DISCORD_MUTATIONS_ENABLED:
                discord_message = await discord_channel.fetch_message(message_id)
                await discord_message.edit(content=message_content)
            else:
                logger_m.warning('Discord mutations not enabled')
        else:
            logger_m.debug(f'Sending message: {message_content}')
            if DISCORD_MUTATIONS_ENABLED:
                await discord_channel.send(content=message_content)
            else:
                logger_m.warning('Discord mutations not enabled')


def prepare_messages(history, scheduled_messages, today):
    messages = []
    past_messages = {message.emoji_prefix: message
                     for message in history
                     if message.emoji_prefix in scheduled_messages}

    # append messages to edit
    for emoji_prefix, message in past_messages.items():
        scheduled_content = f"{emoji_prefix} {scheduled_messages[emoji_prefix]}"
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
    for emoji_prefix, text in scheduled_messages.items():
        if emoji_prefix not in past_messages:
            scheduled_content = f'{emoji_prefix} {text}'
            messages.append((None, scheduled_content))
            break

    return messages


def get_role(guild, id):
    return [role for role in guild.roles if role.id == id][0]
