from pathlib import Path

from scrapy.utils.project import data_path

from juniorguru.lib.scrapers import scrape
from juniorguru.lib import timer
from juniorguru.lib import loggers
from juniorguru.jobs.settings import IMAGES_STORE, HTTPCACHE_DIR, FEEDS


logger = loggers.get('juniorguru.jobs')


class JobsScrapingException(Exception):
    pass


@timer.notify
@timer.measure('jobs')
def main():
    path_jsonl_feed = Path(next(iter(FEEDS.keys())))

    logger.info('Creating directories (to prevent race conditions in spiders)')
    data_path(HTTPCACHE_DIR, createdir=True)
    Path(IMAGES_STORE).mkdir(exist_ok=True, parents=True)
    path_jsonl_feed.parent.mkdir(exist_ok=True, parents=True)

    spider_names = [
        'linkedin',
        'startupjobs',
        'remoteok',
        'weworkremotely',
    ]
    logger.info(f'Scraping {spider_names}')
    scrape('juniorguru.jobs', spider_names)

    logger.info('Checking scrapers')
    if not path_jsonl_feed.exists():
        raise JobsScrapingException("Scrapers didn't save any items")

    logger.info('Scraping done!')


main()
