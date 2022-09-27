from juniorguru.lib.club import run_discord_task
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.sync.club_content import main as club_content_task
from juniorguru.sync.onboarding.channels import manage_channels
from juniorguru.sync.onboarding.messages import send_messages


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.onboarding.discord_task')


@db.connection_context()
async def discord_task(client):
    await manage_channels(client)
    await send_messages(client)
