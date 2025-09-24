from pathlib import Path

import click
from discord import AllowedMentions, Color, Embed, File

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.cache import get_cache
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db, hash_models
from jg.coop.models.sponsor import Sponsor


IMAGES_DIR = Path("jg/coop/images")


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["organizations", "roles"])
@click.option("--channel", "channel_id", default="guide_sponsors", type=parse_channel)
@click.option("--cache-key", default="guide:sponsors")
@click.option("--cache-days", default=30, type=int)
@click.option("--force", is_flag=True, default=False)
def main(channel_id: int, cache_key: str, cache_days: int, force: bool):
    with db.connection_context():
        sponsors = list(Sponsor.club_listing())
    cache = get_cache()
    sponsors_hash = hash_models(sponsors)
    cache_miss = cache.get(cache_key) != sponsors_hash

    if force or cache_miss:
        logger.info(f"Recreating channel! (force={force}, cache_miss={cache_miss})")
        discord_task.run(recreate_channel, channel_id, sponsors)
        cache.set(cache_key, sponsors_hash, expire=86_400 * cache_days)
    else:
        logger.info("Channel is up-to-date")


async def recreate_channel(
    client: ClubClient, channel_id: int, sponsors: list[Sponsor]
):
    channel = await client.fetch_channel(channel_id)
    with mutating_discord(channel) as proxy:
        await proxy.purge(limit=None)
    with mutating_discord(channel) as proxy:
        await proxy.send(
            (
                "# Seznam sponzorů\n\n"
                "Tyto organizace se podílejí na financování junior.guru. "
                "Můžeš se tady prokliknout na jejich stránky. "
                "Sponzorství neznamená, že junior.guru doporučuje konkrétní kurzy, nebo že na ně nemáš psát recenze v klubu. "
                "\n\n"
                "Když sem sponzoři pošlou lidi, tak ti dostanou roli <@&837316268142493736> a k tomu ještě i roli pro konkrétní subjekt, například <@&938306918097747968>. "
                "Role využívej a sponzory klidně označ, pokud po nich něco potřebuješ. "
                "Seznam sponzorů je tady seřazený podle počtu jejich lidí v klubu. "
            ),
            suppress=True,
            allowed_mentions=AllowedMentions.none(),
        )
    for sponsor in sponsors:
        logger.info(f"Posting {sponsor.name!r}")
        embed = Embed(
            title=sponsor.name,
            url=sponsor.url,
            color=Color.dark_grey(),
            description=f"Role: <@&{sponsor.role_id}>\nČlenů: {sponsor.members_count}",
        )
        embed.set_thumbnail(url=f"attachment://{Path(sponsor.poster_path).name}")
        file = File(IMAGES_DIR / sponsor.poster_path)
        with mutating_discord(channel) as proxy:
            await proxy.send(
                embed=embed,
                file=file,
                allowed_mentions=AllowedMentions.none(),
            )
