from datetime import date, timedelta
from pathlib import Path
from pprint import pformat

import click
from discord import Embed, File, ForumChannel, Thread, ui

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.lang import parse_language
from jg.coop.lib.md import md, md_as_text
from jg.coop.lib.mutations import MutationsNotAllowedError, mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.job import ListedJob


JOBS_REPEATING_PERIOD_DAYS = 30

IMAGES_DIR = Path("jg/coop/images")

REASON_ICON_PATH = IMAGES_DIR / "emoji" / "sparkles.png"

UNKNOWN_LOGO_PATH = IMAGES_DIR / "logos-jobs" / "unknown.png"

logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "jobs-locations", "jobs-logos"])
@click.option("--channel", "channel_id", default="jobs", type=parse_channel)
def main(channel_id: int):
    discord_task.run(sync_jobs, channel_id)


@db.connection_context()
async def sync_jobs(client: ClubClient, channel_id: int):
    since_on = date.today() - timedelta(days=JOBS_REPEATING_PERIOD_DAYS)

    logger.debug("Clearing Discord URLs")
    jobs = ListedJob.listing()
    for job in jobs:
        job.discord_url = None
    logger.info(f"Currently listed jobs: {len(jobs)}")

    messages = ClubMessage.forum_listing(channel_id)
    logger.info(f"Found {len(messages)} threads since {since_on}")
    for message in messages:
        if message.created_at.date() > since_on:
            if len(message.ui_urls) > 1:
                raise ValueError(f"Multiple URLs: {message.url} {message.ui_urls!r}")
            try:
                url = message.ui_urls[0]
            except IndexError:
                logger.info(f"Creating manually submitted job: {message.url}")
                try:
                    job = ListedJob.get_by_url(message.url)
                    logger.debug(f"Found, deleting: {job!r}")
                    job.delete_instance()
                except ListedJob.DoesNotExist:
                    pass
                data = get_job_data(message)
                logger.debug(f"Creating:\n{pformat(data)}")
                ListedJob.create(**data)
            else:
                try:
                    job = ListedJob.get_by_url(url)
                    job.discord_url = message.url
                    job.save()
                except ListedJob.DoesNotExist:
                    logger.debug(f"URL to a job no longer listed: {url}")

    jobs = ListedJob.no_discord_listing()
    logger.info(f"Posting {len(jobs)} new jobs to the channel")
    if jobs:
        channel = await client.club_guild.fetch_channel(channel_id)
        for job in jobs:
            logger.debug(f"Posting: {job.effective_url}")
            job.discord_url = await post_job(channel, job)
            job.save()


async def post_job(channel: ForumChannel, job: ListedJob) -> str:
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
    params = dict(
        name=job.title_short,
        content=f"{job.location} — {job.company_name}",
        files=files,
        embeds=embeds,
        view=ui.View(
            ui.Button(emoji="👉", label="Celý inzerát", url=job.effective_url)
        ),
    )

    # create!
    try:
        with mutating_discord(channel, raises=True) as proxy:
            thread: Thread = await proxy.create_thread(**params)
            return thread.jump_url
    except MutationsNotAllowedError:
        return None


def get_job_data(message: ClubMessage) -> dict:
    return dict(
        boards_ids=[f"discord#{message.id}"],
        is_manual=True,
        title=message.channel_name,
        posted_on=message.created_at.date(),
        lang=parse_language(md_as_text(message.content)),
        description_html=md(message.content),
        url=message.url,
        discord_url=message.url,
        company_logo_path=UNKNOWN_LOGO_PATH.relative_to(IMAGES_DIR),
    )
