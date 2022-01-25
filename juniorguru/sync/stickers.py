from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import discord_task, is_discord_mutable


logger = loggers.get('stickers')


STICKERS_CHANNEL = 788823881024405544


@measure('stickers')
@discord_task
async def main(client):
    channel = await client.juniorguru_guild.fetch_channel(STICKERS_CHANNEL)

    async for message in channel.history(limit=None, after=None):
        if not message.stickers:
            continue

        logger.info(f"Found stickers by #{message.author.id}")
        for sticker in message.stickers:
            logger.info(f"Deleting sticker '{sticker.name}'")
        if is_discord_mutable():
            await message.delete()


if __name__ == '__main__':
    main()
