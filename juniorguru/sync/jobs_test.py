from discord import Color, Embed, ui

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED, run_discord_task
from juniorguru.models.base import db


logger = loggers.from_path(__file__)


JOBS_CHANNEL = 1078773263385251860


@cli.sync_command()
def main():
    run_discord_task('juniorguru.sync.jobs_test.discord_task')


@db.connection_context()
async def discord_task(client):
    channel = await client.juniorguru_guild.fetch_channel(JOBS_CHANNEL)
    if DISCORD_MUTATIONS_ENABLED:
        await channel.create_thread('Pokus', 'Tralala',
                                    embed=Embed(title='Embed', color=Color.orange(),
                                                description='Fuuuuuha'),
                                    view=ui.View(ui.Button(emoji='👋',
                                                label='Oujé',
                                                url='https://junior.guru/')))
    else:
        logger.warning('Discord mutations not enabled')
