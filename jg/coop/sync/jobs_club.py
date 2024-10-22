import asyncio
from datetime import date, timedelta
from pathlib import Path

import click
import requests
from discord import Embed, File, ForumChannel, Message, Thread, ui

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.md import md
from jg.coop.lib.mutations import MutationsNotAllowedError, mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.job import DiscordJob, ListedJob


JOBS_REPEATING_PERIOD_DAYS = 30

IMAGES_DIR = Path("jg/coop/images")

REASON_ICON_PATH = IMAGES_DIR / "emoji" / "sparkles.png"

logger = loggers.from_path(__file__)


@cli.sync_command(
    dependencies=[
        "club-content",
        "jobs-logos",
        "jobs-locations",
        "jobs-tech-tags",
    ]
)
@click.option("--channel", "channel_id", default="jobs", type=parse_channel)
def main(channel_id: int):
    discord_task.run(sync_jobs, channel_id)


@db.connection_context()
async def sync_jobs(client: ClubClient, channel_id: int):
    channel = await client.club_guild.fetch_channel(channel_id)
    since_on = date.today() - timedelta(days=JOBS_REPEATING_PERIOD_DAYS)

    logger.debug("Clearing Discord jobs and URLs")
    DiscordJob.drop_table()
    DiscordJob.create_table()
    jobs = ListedJob.listing()
    for job in jobs:
        job.discord_url = None
    logger.info(f"Currently listed jobs: {len(jobs)}")

    messages = ClubMessage.forum_listing(channel_id)
    logger.info(f"Found {len(messages)} threads since {since_on}")
    for message in messages:
        if message.created_at.date() > since_on:
            comments_count = len(ClubMessage.channel_listing(message.channel_id)) - 1
            if len(message.ui_urls) > 1:
                raise ValueError(f"Multiple URLs: {message.url} {message.ui_urls!r}")
            try:
                url = message.ui_urls[0]
            except IndexError:
                logger.info(f"Creating manually submitted job: {message.url}")
                DiscordJob.create(
                    title=message.channel_name,
                    author=message.author,
                    posted_on=message.created_at.date(),
                    description_html=md(message.content),
                    url=message.url,
                    upvotes_count=message.upvotes_count,
                    comments_count=comments_count,
                )
            else:
                thread: Thread = channel.get_thread(message.id)
                try:
                    job = ListedJob.get_by_url(url)
                except ListedJob.DoesNotExist:
                    logger.info(f"Archiving: {url}")
                    await archive_thread(thread)
                else:
                    logger.info(f"Syncing: {url}")
                    job.discord_url = message.url
                    job.upvotes_count = message.upvotes_count
                    job.comments_count = comments_count
                    job.save()
                    await unarchive_thread(thread)
    logger.info(f"Created {DiscordJob.count()} Discord jobs")

    jobs = ListedJob.no_discord_listing()
    logger.info(f"Posting {len(jobs)} new jobs to the channel")
    for job in jobs:
        logger.info(f"Posting: {job.effective_url}")
        job.discord_url = await create_thread(channel, job)
        job.save()


async def archive_thread(thread: Thread) -> None:
    with mutating_discord(thread) as proxy:
        await proxy.archive()


async def unarchive_thread(thread: Thread) -> None:
    if not thread.archived:
        return
    with mutating_discord(thread) as proxy:
        await proxy.unarchive()


async def create_thread(
    channel: ForumChannel, job: ListedJob, sleep_on_retry: int = 3
) -> str:
    try:
        with mutating_discord(channel, raises=True) as proxy:
            for attempt_no in range(1, 4):
                logger.debug(f"Creating thread, attempt #{attempt_no}")
                params = await prepare_thread_params(job)
                thread: Thread = await proxy.create_thread(**params)

                logger.debug("Verifying that images got uploaded correctly")
                message: Message = await thread.fetch_message(thread.id)
                thumbnail_url = message.embeds[0].thumbnail.url
                response = requests.head(thumbnail_url)
                thumbnail_bytes_count = int(response.headers.get("Content-Length", 0))
                if thumbnail_bytes_count == 0:
                    logger.warning(
                        f"Thumbnail is empty (attempt #{attempt_no}): {thumbnail_url}"
                        f" ({thread.name}: {thread.jump_url})"
                    )
                    await thread.delete()
                    await asyncio.sleep(sleep_on_retry)
                else:
                    return thread.jump_url
        logger.error("Failed to create thread!")
        return None
    except MutationsNotAllowedError:
        return None


async def prepare_thread_params(job: ListedJob) -> dict:
    files = []
    embeds = []

    # company
    company_links = [
        f"<:linkedin:915267970752712734> [LinkedIn]({job.company_linkedin_url})",
        f"🔬 [Atmoskop]({job.company_atmoskop_url})",
        f"<:google:976200950886826084> [Google]({job.company_search_url})",
    ]
    if job.company_url:
        company_links.insert(0, f"🏠 [Web]({job.company_url})")
    company_embed = Embed(
        title=job.company_name,
        description="\n".join(company_links),
    )
    if job.company_logo_path:
        files.append(File(IMAGES_DIR.absolute() / job.company_logo_path))
        company_embed.set_thumbnail(
            url=f"attachment://{Path(job.company_logo_path).name}"
        )
    embeds.append(company_embed)

    # reason
    if job.reason:
        files.append(File(REASON_ICON_PATH))
        reason_embed = Embed(description=f"_{job.reason}_")
        reason_embed.set_author(
            name="Proč si můj AI mozeček myslí, že je to juniorní",
            icon_url=f"attachment://{REASON_ICON_PATH.name}",
        )
        embeds.append(reason_embed)

    # job
    return dict(
        name=job.title_short,
        content=f"{job.location} — {job.company_name}",
        files=files,
        embeds=embeds,
        view=ui.View(
            ui.Button(emoji="👉", label="Celý inzerát", url=job.effective_url)
        ),
    )
