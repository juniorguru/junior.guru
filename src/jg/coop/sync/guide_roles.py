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

HEADER_MESSAGE = (
    "# Popis klubových rolí\n\nTady najdeš většinu rolí, které mohou lidi v klubu mít. "
)


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
        logger.info(f"Synchronizing channel (force={force}, cache_miss={cache_miss})")
        discord_task.run(sync_channel, channel_id, roles)
        cache.set(cache_key, roles_hash, expire=86_400 * cache_days)
    else:
        logger.info("Channel is up-to-date")


async def sync_channel(
    client: ClubClient, channel_id: int, roles: list[DocumentedRole]
):
    channel = await client.fetch_channel(channel_id)
    messages = [
        message async for message in channel.history(limit=None, oldest_first=True)
    ]
    if messages:
        header_message = messages[0]
        with mutating_discord(header_message) as proxy:
            await proxy.edit(content=HEADER_MESSAGE, embeds=[], suppress=True)
        role_messages = messages[1:]
    else:
        with mutating_discord(channel) as proxy:
            await proxy.send(content=HEADER_MESSAGE, suppress=True)
        role_messages = []

    for index, role in enumerate(roles):
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

        try:
            message = role_messages[index]
        except IndexError:
            logger.info(f"Posting new message for {role.name!r}")
            with mutating_discord(channel) as proxy:
                await proxy.send(embed=embed, file=file)
        else:
            logger.info(f"Updating message for {role.name!r}")
            with mutating_discord(message) as proxy:
                await proxy.edit(embed=embed, file=file)

    if extra_messages := role_messages[len(roles) :]:
        logger.info(f"Deleting {len(extra_messages)} outdated message(s)")
        for message in extra_messages:
            with mutating_discord(message) as proxy:
                await proxy.delete()
