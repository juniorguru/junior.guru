import textwrap
from datetime import datetime, timedelta

from discord import Embed

from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import discord_task, DISCORD_MUTATIONS_ENABLED
from juniorguru.models import ClubMessage, db


logger = loggers.get('digest')


DIGEST_CHANNEL = 789046675247333397
DIGEST_LIMIT = 5


@measure('digest')
@discord_task
async def main(client):
    week_ago_dt = datetime.utcnow() - timedelta(weeks=1)
    with db:
        last_digest_message = ClubMessage.last_bot_message(DIGEST_CHANNEL, '🔥')
    if last_digest_message:
        since_dt = last_digest_message.created_at
        logger.info(f"Last digest on {since_dt}")
        if since_dt.date() > week_ago_dt.date():
            logger.info(f"Aborting, {since_dt.date()} (last digest) > {week_ago_dt.date()} (week ago)")
            return  # abort
        else:
            logger.info(f"About to create digest, {since_dt.date()} (last digest) <= {week_ago_dt.date()} (week ago)")
    else:
        since_dt = week_ago_dt
        logger.info(f"Last digest not found, analyzing since {week_ago_dt}")

    channel = await client.fetch_channel(DIGEST_CHANNEL)
    with db:
        messages = ClubMessage.digest_listing(since_dt, limit=DIGEST_LIMIT)

    for n, message in enumerate(messages, start=1):
        logger.info(f"Digest #{n}: {message.upvotes_count} votes for {message.author.display_name} in #{message.channel_name}, {message.url}")
    if DISCORD_MUTATIONS_ENABLED:
        content = [
            f"🔥 **{DIGEST_LIMIT} nej příspěvků za uplynulý týden (od {since_dt.day}.{since_dt.month}.)**",
            "",
            "Pokud je něco zajímavé nebo ti to pomohlo, dej tomu palec 👍, srdíčko ❤️, očička 👀, apod. Oceníš autory a pomůžeš tomu, aby se příspěvek mohl objevit i tady. Někomu, kdo nemá čas procházet všechno, co se v klubu napíše, se může tento přehled hodit.",
        ]
        embed_description = []
        for message in messages:
            embed_description += [
                f"{message.upvotes_count}× láska pro {message.author.mention} v {message.channel_mention}:",
                f"> {textwrap.shorten(message.content, 200, placeholder='…')}",
                f"[Hop na příspěvek]({message.url})",
                "",
            ]
        await channel.send(content="\n".join(content),
                           embed=Embed(description="\n".join(embed_description)))
    else:
        logger.warning("Skipping Discord mutations, DISCORD_MUTATIONS_ENABLED not set")


if __name__ == '__main__':
    main()
