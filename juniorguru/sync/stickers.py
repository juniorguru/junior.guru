from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED, run_discord_task
from juniorguru.lib.tasks import sync_task
from juniorguru.sync.club_content import main as club_content_task


STICKERS_CHANNEL = 788823881024405544


logger = loggers.get(__name__)


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.stickers.discord_task')


async def discord_task(client):
    channel = await client.juniorguru_guild.fetch_channel(STICKERS_CHANNEL)

    async for message in channel.history(limit=None, after=None):
        if not message.stickers:
            continue

        logger.info(f"Found stickers by #{message.author.id}")
        for sticker in message.stickers:
            logger.info(f"Deleting sticker '{sticker.name}'")
        if DISCORD_MUTATIONS_ENABLED:
            await message.delete()
        else:
            logger.warning('Discord mutations not enabled')
