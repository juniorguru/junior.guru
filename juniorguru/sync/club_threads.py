from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import mutating
from juniorguru.models.base import db


DEFAULT_AUTO_ARCHIVE_DURATION = 10080  # minutes


logger = loggers.from_path(__file__)


@cli.sync_command()
def main():
    discord_sync.run(discord_task)


@db.connection_context()
async def discord_task(client):
    channels = (channel for channel
                in client.club_guild.channels
                if (hasattr(channel, 'default_auto_archive_duration')
                    and channel.default_auto_archive_duration != DEFAULT_AUTO_ARCHIVE_DURATION
                    and channel.permissions_for(client.club_guild.me).read_messages))
    for channel in channels:
        logger.warning(f'Threads in #{channel.name} auto archive after {channel.default_auto_archive_duration / 60 / 24:.0f} day(s), setting to {DEFAULT_AUTO_ARCHIVE_DURATION / 60 / 24:.0f}')
        with mutating(channel) as proxy:
            await proxy.edit(default_auto_archive_duration=DEFAULT_AUTO_ARCHIVE_DURATION)
