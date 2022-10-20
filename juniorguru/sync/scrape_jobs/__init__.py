from pathlib import Path

from scrapy.utils.project import data_path

from juniorguru.lib import loggers
from juniorguru.lib.scrapers import scrape
from juniorguru.cli.sync import main as cli
from juniorguru.sync.scrape_jobs.feeds import feed_path, feeds_dir
from juniorguru.sync.scrape_jobs.settings import HTTPCACHE_DIR


logger = loggers.get(__name__)


class JobsScrapingException(Exception):
    pass


@cli.sync_command(requires=['proxies'])
def main():
    logger.info('Creating directories (to prevent race conditions in spiders)')
    data_path(HTTPCACHE_DIR, createdir=True)
    Path(feeds_dir()).parent.mkdir(exist_ok=True, parents=True)

    spider_names = [
        'linkedin',
        'startupjobs',
        'remoteok',
        'weworkremotely',
    ]
    logger.info(f'Scraping {spider_names}')
    scrape('juniorguru.sync.scrape_jobs', spider_names)

    logger.info('Checking scrapers')
    # TODO vcucnout scripts/check_scrapers.py
    for spider_name in spider_names:
        path = feed_path(spider_name)
        if not path:
            raise JobsScrapingException(f"Scraper {spider_name} didn't save any items")
        if not path.stat().st_size:
            raise JobsScrapingException(f"Scraper {spider_name} didn't save any items")

    logger.info('Scraping done!')
