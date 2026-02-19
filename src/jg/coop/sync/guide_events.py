from pathlib import Path

import click
from discord import Embed, File, ui

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.cache import get_cache
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db, hash_models
from jg.coop.models.event import Event


IMAGES_DIR = Path("src/jg/coop/images")

HEADER_MESSAGE = (
    "# Záznamy klubových akcí\n\n"
    "Tady najdeš všechny přednášky, které se konaly v klubu. "
    "Videa nejsou „veřejná”, ale pokud chceš odkaz poslat kamarádovi mimo klub, můžeš. "
)


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["events"])
@click.option("--channel", "channel_id", default="guide_events", type=parse_channel)
@click.option("--cache-key", default="guide:events")
@click.option("--cache-days", default=30, type=int)
@click.option("--force", is_flag=True, default=False)
def main(channel_id: int, cache_key: str, cache_days: int, force: bool):
    with db.connection_context():
        events = list(Event.archive_listing())
    cache = get_cache()
    events_hash = hash_models(events)
    cache_miss = cache.get(cache_key) != events_hash

    if force or cache_miss:
        logger.info(f"Synchronizing channel (force={force}, cache_miss={cache_miss})")
        discord_task.run(sync_channel, channel_id, events)
        cache.set(cache_key, events_hash, expire=86_400 * cache_days)
    else:
        logger.info("Channel is up-to-date")


async def sync_channel(client: ClubClient, channel_id: int, events: list[Event]):
    channel = await client.fetch_channel(channel_id)
    messages = [
        message async for message in channel.history(limit=None, oldest_first=True)
    ]
    if messages:
        header_message = messages[0]
        with mutating_discord(header_message) as proxy:
            await proxy.edit(**build_header_args())
        event_messages = messages[1:]
    else:
        with mutating_discord(channel) as proxy:
            await proxy.send(**build_header_args())
        event_messages = []

    for index, event in enumerate(events):
        try:
            message = event_messages[index]
        except IndexError:
            logger.info(f"Posting new message for {event.title!r}")
            with mutating_discord(channel) as proxy:
                await proxy.send(**build_event_args(event))
        else:
            logger.info(f"Updating message for {event.title!r}")
            with mutating_discord(message) as proxy:
                await proxy.edit(**build_event_args(event))

    if extra_messages := event_messages[len(events) :]:
        logger.info(f"Deleting {len(extra_messages)} outdated message(s)")
        for message in extra_messages:
            with mutating_discord(message) as proxy:
                await proxy.delete()


def build_header_args() -> dict:
    return dict(
        content=HEADER_MESSAGE,
        embeds=[],
        view=None,
        suppress=True,
    )


def build_event_args(event: Event) -> dict:
    embed = Embed(
        title=event.title,
        url=event.url,
        timestamp=event.start_at_prg,
    )
    embed.set_author(name=event.bio_name)
    embed.set_thumbnail(url=f"attachment://{Path(event.avatar_path).name}")

    recording_url = event.private_recording_url or event.public_recording_url
    view = ui.View(
        ui.Button(
            emoji="<:youtube:976200175490060299>",
            label="Záznam",
            url=recording_url if recording_url else None,
            disabled=not recording_url,
        )
    )

    return dict(
        embed=embed,
        files=[File(IMAGES_DIR / event.avatar_path)],
        view=view,
    )
