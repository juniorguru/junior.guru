from pathlib import Path

from scrapy.utils.project import data_path

from juniorguru.lib.scrapers import scrape
from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.models import Job, JobDropped, JobError, SpiderMetric, db
from juniorguru.sync.jobs.settings import IMAGES_STORE, HTTPCACHE_DIR


logger = loggers.get('jobs')


@measure('jobs')
def main():
    # If the creation of the directories is left to the spiders, they can end
    # up colliding in making sure it gets created
    data_path(HTTPCACHE_DIR, createdir=True)
    Path(IMAGES_STORE).mkdir(exist_ok=True, parents=True)

    with db:
        db.drop_tables([Job, JobError, JobDropped, SpiderMetric])
        db.create_tables([Job, JobError, JobDropped, SpiderMetric])

    scrape('juniorguru.sync.jobs', [
        'juniorguru',
        # 'linkedin',  # TEMPORARILY DISABLED TO MAKE JOBS FASTER
        'stackoverflow',
        'startupjobs',
        'remoteok',
        'weworkremotely',
        'dobrysef',
    ])
