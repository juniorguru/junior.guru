from juniorguru.lib.tasks import sync_task
from juniorguru.sync import club_content
from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task, is_discord_mutable


STICKERS_CHANNEL = 788823881024405544


logger = loggers.get(__name__)


@sync_task(club_content.main)
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
        if is_discord_mutable():
            await message.delete()
