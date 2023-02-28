import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path

from discord import Embed, File, ui

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.asyncio_extra import chunks
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, JOBS_CHANNEL, fetch_threads,
                                 is_thread_after, run_discord_task)
from juniorguru.models.base import db
from juniorguru.models.job import ListedJob


JOBS_POSTING_CHUNK_SIZE = 2

JOBS_REPEATING_PERIOD_DAYS = 30

PACKAGE_DIR = Path('juniorguru')


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['club-content', 'jobs-locations', 'jobs-logos'])
def main():
    run_discord_task('juniorguru.sync.jobs_club.discord_task')


@db.connection_context()
async def discord_task(client):
    since_at = datetime.now(timezone.utc) - timedelta(days=JOBS_REPEATING_PERIOD_DAYS)
    logger.info(f'Figuring out which jobs are not yet in the channel since {since_at}')
    channel = await client.juniorguru_guild.fetch_channel(JOBS_CHANNEL)
    urls = [get_effective_url(message) async for message
            in fetch_starting_messages(channel, after=since_at)]
    urls = frozenset(filter(None, urls))
    logger.info(f'Found {len(urls)} jobs since {since_at}')
    jobs = [job for job in ListedJob.listing() if job.effective_url not in urls]
    logger.info(f'Posting {len(jobs)} new jobs to the channel')
    jobs_chunks = chunks(jobs, size=JOBS_POSTING_CHUNK_SIZE)
    for n, jobs_chunk in enumerate(jobs_chunks, start=1):
        logger.debug(f'Processing chunk #{n} of {len(jobs_chunk)} jobs')
        await asyncio.gather(*[post_job(channel, job) for job in jobs_chunk])


async def fetch_starting_messages(channel, after=None):
    async for thread in fetch_threads(channel):
        if is_thread_after(thread, after=after):
            yield await thread.fetch_message(thread.id)


def get_effective_url(message):
    try:
        action_row = message.components[0]
        button = action_row.children[0]
        return button.url
    except IndexError:
        return None


async def post_job(channel, job):
    logger[str(job.id)].info(f'Posting {job!r}: {job.effective_url}')
    if DISCORD_MUTATIONS_ENABLED:
        thread = await channel.create_thread(job.title,
                                             job.location,
                                             view=ui.View(ui.Button(emoji='👉',
                                                          label='Mám zájem',
                                                          url=job.effective_url)))
        if job.company_logo_path:
            # https://github.com/Pycord-Development/pycord/issues/1949
            message = thread.get_partial_message(thread.id)
            embed = Embed(title=job.company_name)
            embed.set_thumbnail(url=f"attachment://{Path(job.company_logo_path).name}")
            await message.edit(file=File(PACKAGE_DIR / job.company_logo_path), embed=embed)
    else:
        logger[str(job.id)].warning('Discord mutations not enabled')
