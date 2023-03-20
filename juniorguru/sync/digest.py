import textwrap
from datetime import date, timedelta

from discord import Embed

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import (send_message, ClubChannel,
                                         is_message_older_than)
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage


logger = loggers.from_path(__file__)


DIGEST_LIMIT = 5


@cli.sync_command(dependencies=['club-content'])
def main():
    discord_sync.run(discord_task)


@db.connection_context()
async def discord_task(client):
    since_date = date.today() - timedelta(weeks=1)
    message = ClubMessage.last_bot_message(ClubChannel.ANNOUNCEMENTS, '🔥')
    if is_message_older_than(message, since_date):
        if message:
            since_date = message.created_at.date()
        logger.info(f"Analyzing since {since_date}")

        channel = await client.fetch_channel(ClubChannel.ANNOUNCEMENTS)
        messages = ClubMessage.digest_listing(since_date, limit=DIGEST_LIMIT)

        for n, message in enumerate(messages, start=1):
            logger.info(f"Digest #{n}: {message.upvotes_count} votes for {message.author.display_name} in #{message.channel_name}, {message.url}")

        content = [
            f"🔥 **{DIGEST_LIMIT} nej příspěvků za uplynulý týden (od {since_date:%-d.%-m.})**",
            "",
            "Pokud je něco zajímavé nebo ti to pomohlo, dej tomu palec 👍, srdíčko ❤️, očička 👀, apod. Oceníš autory a pomůžeš tomu, aby se příspěvek mohl objevit i tady. Někomu, kdo nemá čas procházet všechno, co se v klubu napíše, se může tento přehled hodit.",
        ]
        embed_description = []
        for message in messages:
            if message.channel_id == message.parent_channel_id:
                channel_mention = f'<#{message.parent_channel_id}>'
            else:
                channel_mention = f'„{message.channel_name}” (<#{message.parent_channel_id}>)'
            embed_description += [
                f"{message.upvotes_count}× láska pro **{message.author.display_name}** v {channel_mention}:",
                f"> {textwrap.shorten(message.content, 200, placeholder='…')}",
                f"[Hop na příspěvek]({message.url})",
                "",
            ]
        await send_message(channel,
                           content="\n".join(content),
                           embed=Embed(description="\n".join(embed_description)))
