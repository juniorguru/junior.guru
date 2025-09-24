from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import (
    DEFAULT_AUTO_ARCHIVE_DURATION,
    ClubChannelID,
    ClubClient,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db


logger = loggers.from_path(__file__)


@cli.sync_command()
def main():
    discord_task.run(sync_threads)


@db.connection_context()
async def sync_threads(client: ClubClient):
    channels = (
        channel
        for channel in client.club_guild.channels
        if (
            channel.id != ClubChannelID.BOT
            and hasattr(channel, "default_auto_archive_duration")
            and channel.default_auto_archive_duration != DEFAULT_AUTO_ARCHIVE_DURATION
            and channel.permissions_for(client.club_guild.me).read_messages
        )
    )
    for channel in channels:
        logger.warning(
            f"Threads in #{channel.name} auto archive after {channel.default_auto_archive_duration / 60 / 24:.0f} day(s), setting to {DEFAULT_AUTO_ARCHIVE_DURATION / 60 / 24:.0f}"
        )
        with mutating_discord(channel) as proxy:
            await proxy.edit(
                default_auto_archive_duration=DEFAULT_AUTO_ARCHIVE_DURATION
            )
