import os
import subprocess
from multiprocessing import Pool
from pathlib import Path

from juniorguru.lib.log import get_log
from juniorguru.lib import timer, discord_sync
from juniorguru.models import Job, JobDropped, JobError, SpiderMetric, db
from juniorguru.scrapers.settings import IMAGES_STORE


log = get_log('jobs')


JUNIORGURU_GUILD_NUM = 769966886598737931
JOBS_CHANNEL_NUM = 834443926655598592

EMOJI_UPVOTES = ['👍', '❤️']
EMOJI_DOWNVOTES = ['👎']


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

    discord_sync.run(discord_task, os.environ['DISCORD_API_KEY'], intents=['guilds', 'members'])


async def discord_task(client):
    channel = client.get_guild(JUNIORGURU_GUILD_NUM).get_channel(JOBS_CHANNEL_NUM)

    jobs = list(Job.listing())
    seen_links = set()

    async for message in channel.history(limit=None, after=None):
        for job in jobs:
            if job.link.rstrip('/') in message.content:
                log.info(f'Job {job.link} exists')
                seen_links.add(job.link)
                if message.reactions:
                    job.upvotes = sum([r.count for r in message.reactions if r.emoji in EMOJI_UPVOTES])
                    job.downvotes = sum([r.count for r in message.reactions if r.emoji in EMOJI_DOWNVOTES])
                    with db:
                        job.save()
                    log.info(f'Saved {job.link} reactions')

    new_jobs = [job for job in jobs if job.link not in seen_links]
    log.info(f'Posting {len(new_jobs)} new jobs')
    for job in new_jobs:
        content = f'**{job.title}**\n{job.company_name} – {job.location}\n{job.link}'
        await channel.send(content=content)


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
