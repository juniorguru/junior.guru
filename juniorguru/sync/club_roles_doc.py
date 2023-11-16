from datetime import timedelta
from pathlib import Path
import click

from discord import Colour, Embed, File, ui

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import ClubClient, is_message_over_period_ago, parse_channel
from juniorguru.lib.mutations import mutating_discord
from juniorguru.models.base import db
from juniorguru.models.club import ClubDocumentedRole, ClubMessage
from juniorguru.models.event import Event


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "roles"])
@click.option("--channel", "channel_id", default="roles_doc", type=parse_channel)
@click.option("--recreate-interval", 'recreate_interval_days', default=30, type=int, help='In days.')
def main(channel_id: int, recreate_interval_days: int):
    discord_sync.run(recreate_archive, channel_id, recreate_interval_days)


@db.connection_context()
async def recreate_archive(client: ClubClient, channel_id: int, recreate_interval_days: int):
    roles = list(ClubDocumentedRole.listing())
    messages = ClubMessage.channel_listing(channel_id, by_bot=True)
    try:
        last_message = messages[-1]
    except IndexError:
        logger.info("No messages in the channel")
    else:
        if is_message_over_period_ago(last_message, timedelta(days=recreate_interval_days)):
            logger.info("Channel content is too old")
        else:
            logger.info("Channel content is recent, skipping")
            return

    channel = await client.fetch_channel(channel_id)
    with mutating_discord(channel) as proxy:
        await proxy.purge(limit=None)
    with mutating_discord(channel) as proxy:
        await proxy.send(
            "# Seznam klubových rolí\n\n"
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
        # embed.set_author(
        #     name=event.bio_name,
        # )
        if role.icon_url:
            embed.set_thumbnail(url=role.icon_url)
        # embed.set_thumbnail(url=f"attachment://{Path(event.avatar_path).name}")
        # file = File(IMAGES_DIR / event.avatar_path)
        # view = await create_view(event)

        with mutating_discord(channel) as proxy:
            await proxy.send(embed=embed)  # file=file, view=view


async def create_view(
    event: Event,
) -> ui.View:  # View's __init__ touches the event loop
    return ui.View(
        ui.Button(
            emoji="<:youtube:976200175490060299>",
            label="Záznam",
            url=event.recording_url if event.recording_url else None,
            disabled=not event.recording_url,
        )
    )
