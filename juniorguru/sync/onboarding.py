import discord

from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task, JUNIORGURU_BOT
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubUser
from juniorguru.sync.club_content import main as club_content_task


logger = loggers.get(__name__)


ONBOARDING_CHANNELS_CATEGORY = 992438896078110751

MODERATORS_ROLE = 795609174385098762


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.onboarding.discord_task')


@db.connection_context()
async def discord_task(client):
    category = await client.fetch_channel(ONBOARDING_CHANNELS_CATEGORY)
    permissions = {
        client.juniorguru_guild.default_role: discord.PermissionOverwrite(read_messages=False),
        (await client.get_or_fetch_user(JUNIORGURU_BOT)): discord.PermissionOverwrite(read_messages=True),
        get_role(client.juniorguru_guild, MODERATORS_ROLE): discord.PermissionOverwrite(read_messages=True),
    }

    for member in ClubUser.members_listing():
        # TODO member: discord.PermissionOverwrite(read_messages=True),
        # channel = await client.juniorguru_guild.create_text_channel(name='test',
        #                                                             topic='prdíme!',
        #                                                             category=category,
        #                                                             overwrites=permissions)
        category, permissions
        break


def get_role(guild, id):
    return [role for role in guild.roles if role.id == id][0]
