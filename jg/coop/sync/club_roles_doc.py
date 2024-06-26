from datetime import timedelta
from pathlib import Path

import click
from discord import Colour, Embed, File

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import (
    ClubClient,
    is_message_over_period_ago,
    parse_channel,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.documented_role import DocumentedRole


IMAGES_DIR = Path("jg/coop/images")


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "roles"])
@click.option("--channel", "channel_id", default="roles_doc", type=parse_channel)
@click.option(
    "--recreate-interval",
    "recreate_interval_days",
    default=30,
    type=int,
    help="In days.",
)
def main(channel_id: int, recreate_interval_days: int):
    discord_task.run(recreate_archive, channel_id, recreate_interval_days)


@db.connection_context()
async def recreate_archive(
    client: ClubClient, channel_id: int, recreate_interval_days: int
):
    roles = list(DocumentedRole.listing())
    messages = ClubMessage.channel_listing(channel_id, by_bot=True)
    try:
        last_message = messages[-1]
    except IndexError:
        logger.info("No messages in the channel")
    else:
        if is_message_over_period_ago(
            last_message, timedelta(days=recreate_interval_days)
        ):
            logger.info("Channel content is too old")
        else:
            logger.info("Channel content is recent, skipping")
            return

    channel = await client.fetch_channel(channel_id)
    with mutating_discord(channel) as proxy:
        await proxy.purge(limit=None)
    with mutating_discord(channel) as proxy:
        await proxy.send(
            "# Popis klubových rolí\n\n"
            "Tady najdeš většinu rolí, které mohou lidi v klubu mít. ",
            suppress=True,
        )
    for role in logger.progress(roles, chunk_size=10):
        logger.info(f"Posting {role.name!r}")
        embed = Embed(
            title=role.name,
            color=Colour(role.color),
            description=role.description,
        )
        if role.icon_path:
            path = IMAGES_DIR / role.icon_path
            logger.debug(f"Setting thumbnail: {path}")
            embed.set_thumbnail(url=f"attachment://{path.name}")
            file = File(path)
        else:
            logger.debug(f"Setting no thumbnail, role.icon_path is {role.icon_path!r}")
            file = None

        with mutating_discord(channel) as proxy:
            await proxy.send(embed=embed, file=file)
