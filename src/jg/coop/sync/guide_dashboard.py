from pathlib import Path

import click
from discord import Embed, ui

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.cache import get_cache
from jg.coop.lib.discord_club import (
    CLUB_GUILD_ID,
    ClubChannelID,
    ClubClient,
    parse_channel,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.lib.text import emoji_url
from jg.coop.models.base import db, hash_models
from jg.coop.models.tip import Tip


IMAGES_DIR = Path("src/jg/coop/images")

HEADER_MESSAGE = (
    "# Pravidla a tipy\n\n"
    "Klub je místo, kde můžeš spolu s ostatními posunout svůj rozvoj v oblasti programování, "
    "nebo s tím pomoci ostatním.\n\n"
    "👉 Tykáme si\n"
    "👉 Dodržuj pravidla chování na [junior.guru/coc](https://junior.guru/coc/)"
)

LINKS_MESSAGE = "## Odkazy"

LINKS_VIEW = ui.View(
    ui.Button(
        emoji="💳",
        label="Nastavení placení",
        url="https://juniorguru.memberful.com",
    ),
    ui.Button(
        emoji="🤔",
        label="Časté dotazy",
        url="https://junior.guru/faq/",
    ),
    ui.Button(
        emoji="💕",
        label="Pravidla chování",
        url="https://junior.guru/coc/",
    ),
    ui.Button(
        emoji="💡",
        label="Zpětná vazba",
        url=f"https://discord.com/channels/{CLUB_GUILD_ID}/{ClubChannelID.META}",
    ),
)

TIPS_HEADER_MESSAGE = (
    "## Tipy\n\n"
    "Jak z klubu dostat maximum? Tady je seznam tipů, které ti pomohou se zorientovat. "
    f"Najdeš je také v <#{ClubChannelID.TIPS}>"
)


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["tips"])
@click.option("--channel", "channel_id", default="guide_dashboard", type=parse_channel)
@click.option("--cache-key", default="guide:dashboard")
@click.option("--cache-days", default=30, type=int)
@click.option("--force", is_flag=True, default=False)
def main(channel_id: int, cache_key: str, cache_days: int, force: bool):
    with db.connection_context():
        tips = list(Tip.listing())
    cache = get_cache()
    tips_hash = hash_models(tips)
    cache_miss = cache.get(cache_key) != tips_hash

    if force or cache_miss:
        logger.info(f"Synchronizing channel (force={force}, cache_miss={cache_miss})")
        discord_task.run(sync_channel, channel_id, tips)
        cache.set(cache_key, tips_hash, expire=86_400 * cache_days)
    else:
        logger.info("Channel is up-to-date")


async def sync_channel(client: ClubClient, channel_id: int, tips: list[Tip]):
    channel = await client.fetch_channel(channel_id)
    messages = [
        message async for message in channel.history(limit=None, oldest_first=True)
    ]
    if messages:
        header_message = messages[0]
        with mutating_discord(header_message) as proxy:
            await proxy.edit(
                content=HEADER_MESSAGE,
                embeds=[],
                suppress=True,
            )
        links_message = messages[1] if len(messages) > 1 else None
        if links_message:
            with mutating_discord(links_message) as proxy:
                await proxy.edit(content=LINKS_MESSAGE, embeds=[], view=LINKS_VIEW)
        tips_header_message = messages[2] if len(messages) > 2 else None
        if tips_header_message:
            with mutating_discord(tips_header_message) as proxy:
                await proxy.edit(
                    content=TIPS_HEADER_MESSAGE,
                    embeds=[],
                    suppress=True,
                )
        tip_messages = messages[3:]
    else:
        with mutating_discord(channel) as proxy:
            await proxy.send(content=HEADER_MESSAGE, suppress=True)
            await proxy.send(content=LINKS_MESSAGE, view=LINKS_VIEW)
            await proxy.send(content=TIPS_HEADER_MESSAGE, suppress=True)
        tip_messages = []

    for index, tip in enumerate(tips):
        embed = Embed(
            title=tip.title_text,
            url=tip.discord_url,
            description=tip.lead,
        )
        embed.set_thumbnail(url=emoji_url(tip.emoji))

        try:
            message = tip_messages[index]
        except IndexError:
            logger.info(f"Posting new message for {tip.title!r}")
            with mutating_discord(channel) as proxy:
                await proxy.send(embed=embed)
        else:
            logger.info(f"Updating message for {tip.title!r}")
            with mutating_discord(message) as proxy:
                await proxy.edit(embed=embed)

    if extra_messages := tip_messages[len(tips) :]:
        logger.info(f"Deleting {len(extra_messages)} outdated message(s)")
        for message in extra_messages:
            with mutating_discord(message) as proxy:
                await proxy.delete()
