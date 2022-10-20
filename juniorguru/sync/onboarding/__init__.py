from juniorguru.lib.club import run_discord_task
from juniorguru.cli.sync import main as cli
from juniorguru.models.base import db
from juniorguru.sync.onboarding.channels import manage_channels
from juniorguru.sync.onboarding.messages import send_messages


@cli.sync_command(requires=['club-content'])
def main():
    run_discord_task('juniorguru.sync.onboarding.discord_task')


@db.connection_context()
async def discord_task(client):
    await manage_channels(client)
    await send_messages(client)
