import re
from datetime import date

import discord
from slugify import slugify

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

MESSAGES = [
    ('👋', 'Smrdíme v klubu!'),
    ('🌯', 'Žereme burrito'),
    ('💤', 'Spíme'),
    ('🆗', 'Jsme OK'),
    ('🟡', 'Hele žluté kolečko'),
    ('🟥', 'Hele červený čtvereček'),
    ('🤡', 'Klauni toto!'),
]




@sync_task(club_content_task)
def main():
    if len([emoji for emoji, _ in MESSAGES]) != len({emoji for emoji, _ in MESSAGES}):
        raise ValueError('Emojis of onboarding messages must be unique!')

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
    for member in ClubUser.members_listing():
        if member.id != 652142810291765248:  # TODO
            continue

        logger_m = logger.getChild(f'members.{member.id}')
        if not member.onboarding_channel_id:
            logger_m.warning("Missing onboarding channel, skipping!")
            continue
        discord_channel = None
        last_message_on = None
        for emoji, message_content in MESSAGES:
            message = ClubMessage.last_bot_message(member.onboarding_channel_id, emoji)
            message_content = f'{emoji} {message_content}'
            if message:
                last_message_on = message.created_at.date()
                if message.content == message_content:
                    logger_m.info(f'Message {emoji} already exists')
                else:
                    logger_m.info(f'Message {emoji} needs updates')
                    if not discord_channel:
                        discord_channel = await client.fetch_channel(member.onboarding_channel_id)
                    discord_message = await discord_channel.fetch_message(message.id)
                    await discord_message.edit(content=message_content)
            else:
                logger_m.info(f'Message {emoji} needs to be sent')
                logger_m.debug(f'Last message sent on: {last_message_on}')
                if not last_message_on or last_message_on < today:
                    logger_m.debug(f'Sending message {emoji}')
                    if not discord_channel:
                        discord_channel = await client.fetch_channel(member.onboarding_channel_id)
                    await discord_channel.send(content=message_content)
                else:
                    logger_m.info(f'Sending message {emoji} canceled, will send tomorrow')
                break

def get_role(guild, id):
    return [role for role in guild.roles if role.id == id][0]
