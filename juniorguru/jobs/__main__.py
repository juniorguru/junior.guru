from pathlib import Path

from scrapy.utils.project import data_path

from juniorguru.lib.scrapers import scrape
from juniorguru.lib import timer
from juniorguru.lib import loggers
from juniorguru.jobs.settings import IMAGES_STORE, HTTPCACHE_DIR, FEEDS


logger = loggers.get('jobs')


@timer.notify
@timer.measure('jobs')
def main():
    # If the creation of the directories is left to the spiders, they
    # can race condition during directory creation
    paths = [Path(IMAGES_STORE)] + [Path(path).parent for path in FEEDS.keys()]
    for path in paths:
        path.mkdir(exist_ok=True, parents=True)
    data_path(HTTPCACHE_DIR, createdir=True)  # special case

    scrape('juniorguru.jobs', [
        'linkedin',
        'startupjobs',
        'remoteok',
        'weworkremotely',
    ])


main()
