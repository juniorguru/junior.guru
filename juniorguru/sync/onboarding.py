import re

import discord
from slugify import slugify

from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task, JUNIORGURU_BOT, DISCORD_MUTATIONS_ENABLED
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubUser
from juniorguru.sync.club_content import main as club_content_task


logger = loggers.get(__name__)


CHANNEL_TOPIC_RE = re.compile(r'\#(?P<id>\d+)\s*$')

ONBOARDING_CHANNELS_CATEGORY = 992438896078110751

MODERATORS_ROLE = 795609174385098762


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.onboarding.discord_task')


@db.connection_context()
async def discord_task(client):
    category = await client.fetch_channel(ONBOARDING_CHANNELS_CATEGORY)
    member_channel_mapping = {}

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
            logger.info(f"Channel #{channel.name} identified as personal channel of member #{member_id}")
            member_channel_mapping[int(member_id)] = channel

    permissions = {
        client.juniorguru_guild.default_role: discord.PermissionOverwrite(read_messages=False),
        (await client.get_or_fetch_user(JUNIORGURU_BOT)): discord.PermissionOverwrite(read_messages=True),
        get_role(client.juniorguru_guild, MODERATORS_ROLE): discord.PermissionOverwrite(read_messages=True),
    }
    for member in ClubUser.members_listing():
        if member.id != 652142810291765248:  # TODO
            continue

        try:
            channel = member_channel_mapping[member.id]
            logger.info(f"Personal channel of member #{member.id} already exists")
        except KeyError:
            logger.info(f"Personal channel of member #{member.id} needs to be created")
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


def get_role(guild, id):
    return [role for role in guild.roles if role.id == id][0]
