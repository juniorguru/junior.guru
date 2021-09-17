from pathlib import Path

from scrapy.utils.project import data_path

from juniorguru.lib import scrapers
from juniorguru.lib.timer import measure
from juniorguru.lib.log import get_log
from juniorguru.lib.club import discord_task, count_downvotes, count_upvotes, DISCORD_MUTATIONS_ENABLED
from juniorguru.models import Job, JobDropped, JobError, SpiderMetric, db
from juniorguru.sync.jobs.settings import IMAGES_STORE, HTTPCACHE_DIR


log = get_log('jobs')


JOBS_CHANNEL = 834443926655598592
JOBS_VOTING_CHANNEL = 841680291675242546


@measure('jobs')
def main():
    # If the creation of the directories is left to the spiders, they can end
    # up colliding in making sure it gets created
    data_path(HTTPCACHE_DIR, createdir=True)
    Path(IMAGES_STORE).mkdir(exist_ok=True, parents=True)

    with db:
        db.drop_tables([Job, JobError, JobDropped, SpiderMetric])
        db.create_tables([Job, JobError, JobDropped, SpiderMetric])

    scrapers.run_many('juniorguru.sync.jobs', [
        'juniorguru',
        'linkedin',
        'stackoverflow',
        'startupjobs',
        'remoteok',
        'wwr',
        'dobrysef',
    ])

    manage_jobs_channel()


@discord_task
async def manage_jobs_channel(client):
    channel = await client.fetch_channel(JOBS_CHANNEL)

    jobs = list(Job.listing())
    seen_links = set()

    async for message in channel.history(limit=None, after=None):
        for job in jobs:
            if job.link.rstrip('/') in message.content:
                log.info(f'Job {job.link} exists')
                seen_links.add(job.link)
                if message.reactions:
                    job.upvotes_count = count_upvotes(message.reactions)
                    job.downvotes_count = count_downvotes(message.reactions)
                    with db:
                        job.save()
                    log.info(f'Saved {job.link} reactions')

    if DISCORD_MUTATIONS_ENABLED:
        new_jobs = [job for job in jobs if job.link not in seen_links]
        log.info(f'Posting {len(new_jobs)} new jobs')
        for job in new_jobs:
            await channel.send(f'**{job.title}**\n{job.company_name} – {job.location}\n{job.link}')
    else:
        log.warning("Skipping Discord mutations, DISCORD_MUTATIONS_ENABLED not set")


@discord_task
async def manage_jobs_voting_channel(client):  # experimenting with Mila and ML
    channel = await client.fetch_channel(JOBS_VOTING_CHANNEL)
    seen_links = set()

    log.info('Processing voting for jobs')
    jobs = list(Job.select().where(Job.magic_is_junior == False))  # TODO PoC, move this to models or revamp models altogether?
    async for message in channel.history(limit=None, after=None):
        for job in jobs:
            link = job.link
            if link.rstrip('/') in message.content:
                log.info(f'Job {link} exists')
                seen_links.add(link)
                if message.reactions:
                    job.upvotes_count += count_upvotes(message.reactions)
                    job.downvotes_count += count_downvotes(message.reactions)
                    with db:
                        job.save()
                    log.info(f'Saved {link} reactions')

    log.info('Processing voting for dropped jobs')
    jobs_dropped = list(JobDropped.select().where(JobDropped.magic_is_junior == True))  # TODO PoC, move this to models or revamp models altogether?
    async for message in channel.history(limit=None, after=None):
        for job_dropped in jobs_dropped:
            link = job_dropped.item['link']
            if link.rstrip('/') in message.content:
                log.info(f'Job {link} exists')
                seen_links.add(link)
                if message.reactions:
                    job_dropped.upvotes_count += count_upvotes(message.reactions)
                    job_dropped.downvotes_count += count_downvotes(message.reactions)
                    with db:
                        job_dropped.save()
                    log.info(f'Saved {link} reactions')

    if DISCORD_MUTATIONS_ENABLED:
        new_jobs = [job for job in jobs if job.link not in seen_links]
        log.info(f'Posting {len(new_jobs)} new jobs')
        for job in new_jobs:
            await channel.send(f'**{job.title}**\n{job.company_name} – {job.location}\n{job.link}')

        new_jobs_dropped = [job_dropped for job_dropped in jobs_dropped if job_dropped.item['link'] not in seen_links]
        log.info(f'Posting {len(new_jobs_dropped)} new dropped jobs')
        for job_dropped in new_jobs_dropped:
            await channel.send(f"**{job_dropped.item['title']}**\n{job_dropped.item['company_name']} – {', '.join(job_dropped.item['locations_raw'])}\n{job_dropped.item['link']}")
    else:
        log.warning("Skipping Discord mutations, DISCORD_MUTATIONS_ENABLED not set")
