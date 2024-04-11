from datetime import timedelta
from pathlib import Path

import click
from discord import Embed, File, ui

from project.cli.sync import main as cli
from project.lib import discord_task, loggers
from project.lib.discord_club import (
    ClubClient,
    is_message_over_period_ago,
    parse_channel,
)
from project.lib.mutations import mutating_discord
from project.models.base import db
from project.models.club import ClubMessage
from project.models.event import Event


IMAGES_DIR = Path("project/images")


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "events"])
@click.option("--channel", "channel_id", default="events_archive", type=parse_channel)
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
    events = list(Event.archive_listing())
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
            "# Záznamy klubových akcí\n\n"
            "Tady najdeš všechny přednášky, které se konaly v klubu. "
            "Videa nejsou „veřejná”, ale pokud chceš odkaz poslat kamarádovi mimo klub, můžeš. ",
            suppress=True,
        )
    for event in logger.progress(events, chunk_size=10):
        logger.info(f"Posting {event.title!r}")
        embed = Embed(
            title=event.title,
            url=event.url,
            timestamp=event.start_at_prg,
        )
        embed.set_author(
            name=event.bio_name,
        )
        embed.set_thumbnail(url=f"attachment://{Path(event.avatar_path).name}")
        file = File(IMAGES_DIR / event.avatar_path)
        view = await create_view(event)

        with mutating_discord(channel) as proxy:
            await proxy.send(embed=embed, file=file, view=view)


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
