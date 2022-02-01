from pathlib import Path

from scrapy.utils.project import data_path

from juniorguru.lib.scrapers import scrape
from juniorguru.lib import timer
from juniorguru.lib import loggers
from juniorguru.jobs.settings import IMAGES_STORE, HTTPCACHE_DIR


logger = loggers.get('jobs')


@timer.notify
@timer.measure('jobs')
def main():
    # If the creation of the directories is left to the spiders, they can end
    # up colliding in making sure it gets created
    data_path(HTTPCACHE_DIR, createdir=True)
    Path(IMAGES_STORE).mkdir(exist_ok=True, parents=True)

    scrape('juniorguru.jobs', [
        # 'juniorguru',
        'linkedin',
        'stackoverflow',
        'startupjobs',
        'remoteok',
        'weworkremotely',
        'dobrysef',
    ])


main()
