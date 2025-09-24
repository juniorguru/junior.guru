from pathlib import Path

import click
from discord import Colour, Embed, File

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.cache import get_cache
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.mutations import mutating_discord
from jg.coop.lib.text import emoji_url
from jg.coop.models.base import db, hash_models
from jg.coop.models.role import DocumentedRole


IMAGES_DIR = Path("src/jg/coop/images")


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["roles"])
@click.option("--channel", "channel_id", default="guide_roles", type=parse_channel)
@click.option("--cache-key", default="guide:roles")
@click.option("--cache-days", default=30, type=int)
@click.option("--force", is_flag=True, default=False)
def main(channel_id: int, cache_key: str, cache_days: int, force: bool):
    with db.connection_context():
        roles = list(DocumentedRole.listing())
    cache = get_cache()
    roles_hash = hash_models(roles, exclude=[DocumentedRole.id])
    cache_miss = cache.get(cache_key) != roles_hash

    if force or cache_miss:
        logger.info(f"Recreating channel! (force={force}, cache_miss={cache_miss})")
        discord_task.run(recreate_channel, channel_id, roles)
        cache.set(cache_key, roles_hash, expire=86_400 * cache_days)
    else:
        logger.info("Channel is up-to-date")


async def recreate_channel(
    client: ClubClient, channel_id: int, roles: list[DocumentedRole]
):
    channel = await client.fetch_channel(channel_id)
    with mutating_discord(channel) as proxy:
        await proxy.purge(limit=None)
    with mutating_discord(channel) as proxy:
        await proxy.send(
            "# Popis klubových rolí\n\n"
            "Tady najdeš většinu rolí, které mohou lidi v klubu mít. ",
            suppress=True,
        )
    for role in roles:
        logger.info(f"Posting {role.name!r}")
        embed = Embed(
            title=role.name,
            color=Colour(role.color),
            description=role.description,
        )
        file = None
        if role.icon_path:
            path = IMAGES_DIR / role.icon_path
            logger.debug(f"Setting thumbnail: {path}")
            embed.set_thumbnail(url=f"attachment://{path.name}")
            file = File(path)
        elif role.emoji:
            logger.debug(f"Setting emoji thumbnail: {role.emoji}")
            embed.set_thumbnail(url=emoji_url(role.emoji))
        else:
            logger.debug(f"Setting no thumbnail, role.icon_path is {role.icon_path!r}")
        with mutating_discord(channel) as proxy:
            await proxy.send(embed=embed, file=file)
