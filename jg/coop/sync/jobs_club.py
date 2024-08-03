import asyncio
import textwrap
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import AsyncGenerator

from discord import Embed, File, ForumChannel, Message, ui

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.chunks import chunks
from jg.coop.lib.discord_club import (
    ClubChannelID,
    ClubClient,
    fetch_threads,
    is_thread_after,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.job import ListedJob


JOBS_POSTING_CHUNK_SIZE = 2

JOBS_REPEATING_PERIOD_DAYS = 30

IMAGES_DIR = Path("jg/coop/images")


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "jobs-locations", "jobs-logos"])
def main():
    discord_task.run(sync_jobs)


# TODO use club content, see how weekly plans are done
@db.connection_context()
async def sync_jobs(client: ClubClient):
    since_at = datetime.now(timezone.utc) - timedelta(days=JOBS_REPEATING_PERIOD_DAYS)
    logger.info(f"Figuring out which jobs are not yet in the channel since {since_at}")
    channel = await client.club_guild.fetch_channel(ClubChannelID.JOBS)
    urls = [
        get_effective_url(message)
        async for message in fetch_starting_messages(channel, after=since_at)
    ]
    urls = frozenset(filter(None, urls))
    logger.info(f"Found {len(urls)} jobs since {since_at}")
    jobs = [job for job in ListedJob.listing() if job.effective_url not in urls]
    logger.info(f"Posting {len(jobs)} new jobs to the channel")
    jobs_chunks = chunks(jobs, size=JOBS_POSTING_CHUNK_SIZE)
    for n, jobs_chunk in enumerate(jobs_chunks, start=1):
        logger.debug(f"Processing chunk #{n} of {len(jobs_chunk)} jobs")
        await asyncio.gather(*[post_job(channel, job) for job in jobs_chunk])


async def fetch_starting_messages(
    channel: ForumChannel, after: date | None = None
) -> AsyncGenerator[Message, None]:
    async for thread in fetch_threads(channel):
        if is_thread_after(thread, after=after):
            yield await thread.fetch_message(thread.id)


def get_effective_url(message: Message) -> str | None:
    try:
        action_row = message.components[0]
        button = action_row.children[0]
        return button.url
    except IndexError:
        return None


async def post_job(channel: ForumChannel, job: ListedJob):
    logger[str(job.id)].info(f"Posting {job!r}: {job.effective_url}")
    title = textwrap.shorten(job.title, 90, placeholder="…")
    embed = Embed(title=job.company_name)
    params = dict(
        title=title,
        content=job.location,
        embed=embed,
        view=ui.View(ui.Button(emoji="👉", label="Zjistit víc", url=job.effective_url)),
    )
    if job.company_logo_path:
        embed.set_thumbnail(url=f"attachment://{Path(job.company_logo_path).name}")
        params["file"] = File(IMAGES_DIR.absolute() / job.company_logo_path)
    with mutating_discord(channel) as proxy:
        await proxy.create_thread(**params)
