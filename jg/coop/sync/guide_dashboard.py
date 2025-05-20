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


IMAGES_DIR = Path("jg/coop/images")


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
        logger.info(f"Recreating channel! (force={force}, cache_miss={cache_miss})")
        discord_task.run(recreate_channel, channel_id, tips)
        cache.set(cache_key, tips_hash, expire=86_400 * cache_days)
    else:
        logger.info("Channel is up-to-date")


async def recreate_channel(client: ClubClient, channel_id: int, tips: list[Tip]):
    channel = await client.fetch_channel(channel_id)
    with mutating_discord(channel) as proxy:
        await proxy.purge(limit=None)
        await proxy.send(
            (
                "# Pravidla a tipy\n\n"
                "Klub je místo, kde můžeš spolu s ostatními posunout svůj rozvoj v oblasti programování, "
                "nebo s tím pomoci ostatním.\n\n"
                "👉 Tykáme si\n"
                "👉 Dodržuj pravidla chování na [junior.guru/coc](https://junior.guru/coc/)"
            ),
            suppress=True,
        )
        await proxy.send(
            "## Odkazy",
            view=ui.View(
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
            ),
        )
        await proxy.send(
            (
                "## Tipy\n\n"
                "Jak z klubu dostat maximum? Tady je seznam tipů, které ti pomohou se zorientovat. "
                f"Najdeš je také v <#{ClubChannelID.TIPS}>"
            ),
            suppress=True,
        )
    for tip in tips:
        logger.info(f"Posting {tip.title!r}")
        embed = Embed(
            title=tip.title_text,
            url=tip.discord_url,
            description=tip.lead,
        )
        embed.set_thumbnail(url=emoji_url(tip.emoji))
        with mutating_discord(channel) as proxy:
            await proxy.send(embed=embed)
