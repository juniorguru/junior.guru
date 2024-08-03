import itertools
from datetime import date, timedelta
from pathlib import Path

import click
from discord import Embed, File, ForumChannel, ui

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.job import ListedJob


JOBS_REPEATING_PERIOD_DAYS = 30

IMAGES_DIR = Path("jg/coop/images")


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "jobs-locations", "jobs-logos"])
@click.option("--channel", "channel_id", default="jobs", type=parse_channel)
def main(channel_id: int):
    discord_task.run(sync_jobs, channel_id)


@db.connection_context()
async def sync_jobs(client: ClubClient, channel_id: int):
    since_on = date.today() - timedelta(days=JOBS_REPEATING_PERIOD_DAYS)
    messages = [
        message
        for message in ClubMessage.forum_listing(channel_id)
        if message.created_at.date() > since_on
    ]
    logger.info(f"Found {len(messages)} threads since {since_on}")
    urls = frozenset(
        itertools.chain.from_iterable(message.ui_urls for message in messages)
    )
    logger.info(f"Found {len(urls)} job URLs since {since_on}")
    jobs = [job for job in ListedJob.listing() if job.effective_url not in urls]
    if jobs:
        logger.info(f"Posting {len(jobs)} new jobs to the channel")
        channel = await client.club_guild.fetch_channel(channel_id)
        for job in jobs:
            logger.info(f"Posting: {job.effective_url}")
            await post_job(channel, job)
    else:
        logger.info("No new jobs to post")


async def post_job(channel: ForumChannel, job: ListedJob):
    embed = Embed(title=job.company_name)
    params = dict(
        name=job.title_short,
        content=job.location,
        embed=embed,
        view=ui.View(ui.Button(emoji="👉", label="Zjistit víc", url=job.effective_url)),
    )
    if job.company_logo_path:
        embed.set_thumbnail(url=f"attachment://{Path(job.company_logo_path).name}")
        params["file"] = File(IMAGES_DIR.absolute() / job.company_logo_path)
    with mutating_discord(channel) as proxy:
        await proxy.create_thread(**params)
