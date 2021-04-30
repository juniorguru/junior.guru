import subprocess
from multiprocessing import Pool
from pathlib import Path

from juniorguru.lib.log import get_log
from juniorguru.lib import timer
from juniorguru.lib.club import discord_task, count_downvotes, count_upvotes, DISCORD_MUTATIONS_ENABLED
from juniorguru.models import Job, JobDropped, JobError, SpiderMetric, db
from juniorguru.scrapers.settings import IMAGES_STORE


log = get_log('jobs')


@timer.notify
def main():
    # If the creation of the directory is left to the spiders, they can end
    # up colliding in making sure it gets created
    Path(IMAGES_STORE).mkdir(exist_ok=True, parents=True)

    with db:
        db.drop_tables([Job, JobError, JobDropped, SpiderMetric])
        db.create_tables([Job, JobError, JobDropped, SpiderMetric])

    spider_names = [
        'juniorguru',
        'linkedin',
        'stackoverflow',
        'startupjobs',
        'remoteok',
        'wwr',
        'dobrysef',
    ]
    Pool().map(run_spider, spider_names)

    manage_jobs_channel()


@discord_task
async def manage_jobs_channel(client):
    channel = await client.fetch_channel('práce-bot')

    jobs = list(Job.listing())
    seen_links = set()

    async for message in channel.history(limit=None, after=None):
        for job in jobs:
            if job.link.rstrip('/') in message.content:
                log.info(f'Job {job.link} exists')
                seen_links.add(job.link)
                if message.reactions:
                    job.upvotes = count_upvotes(message.reactions)
                    job.downvotes = count_downvotes(message.reactions)
                    with db:
                        job.save()
                    log.info(f'Saved {job.link} reactions')

    if DISCORD_MUTATIONS_ENABLED:
        new_jobs = [job for job in jobs if job.link not in seen_links]
        log.info(f'Posting {len(new_jobs)} new jobs')
        for job in new_jobs:
            await channel.send(f'**{job.title}**\n{job.company_name} – {job.location}\n{job.link}')


def run_spider(spider_name):
    proc = subprocess.Popen(['scrapy', 'crawl', spider_name], text=True, bufsize=1,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        for line in proc.stdout:
            print(f'[jobs/{spider_name}] {line}', end='')
    except KeyboardInterrupt:
        proc.kill()
        proc.communicate()


if __name__ == '__main__':
    main()
