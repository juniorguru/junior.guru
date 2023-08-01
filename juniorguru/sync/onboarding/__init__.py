from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync
from juniorguru.lib.discord_club import ClubClient
from juniorguru.models.base import db
from juniorguru.sync.onboarding.channels import manage_channels
from juniorguru.sync.onboarding.messages import send_messages


@cli.sync_command(dependencies=['club-content'])
def main():
    discord_sync.run(discord_task)


@db.connection_context()
async def discord_task(client: ClubClient):
    await manage_channels(client)
    await send_messages(client)
