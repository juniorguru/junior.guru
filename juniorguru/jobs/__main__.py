from pathlib import Path

from scrapy.utils.project import data_path

from juniorguru.lib.scrapers import scrape
from juniorguru.lib import timer
from juniorguru.lib import loggers
from juniorguru.jobs.settings import IMAGES_STORE, HTTPCACHE_DIR, FEEDS


logger = loggers.get('juniorguru.jobs')


FEED_URI_TEMPLATE = next(iter(FEEDS.keys()))


class JobsScrapingException(Exception):
    pass


@timer.notify
@timer.measure('jobs')
def main():
    logger.info('Creating directories (to prevent race conditions in spiders)')
    data_path(HTTPCACHE_DIR, createdir=True)
    Path(IMAGES_STORE).mkdir(exist_ok=True, parents=True)
    Path(FEED_URI_TEMPLATE).parent.mkdir(exist_ok=True, parents=True)

    spider_names = [
        'linkedin',
        'startupjobs',
        'remoteok',
        'weworkremotely',
    ]
    logger.info(f'Scraping {spider_names}')
    scrape('juniorguru.jobs', spider_names)

    logger.info('Checking scrapers')
    # TODO vcucnout scripts/check_scrapers.py
    for spider_name in spider_names:
        feed_path = Path(FEED_URI_TEMPLATE % dict(name=spider_name))
        if not feed_path:
            raise JobsScrapingException(f"Scraper {spider_name} didn't save any items")
        if not feed_path.stat().st_size:
            raise JobsScrapingException(f"Scraper {spider_name} didn't save any items")

    logger.info('Scraping done!')


main()
