from pathlib import Path

from scrapy.utils.project import data_path

from juniorguru.lib.scrapers import scrape
from juniorguru.lib.tasks import sync_task
from juniorguru.lib import loggers
from juniorguru.sync.scrape_companies.settings import HTTPCACHE_DIR, IMAGES_STORE


logger = loggers.get(__name__)


@sync_task(name='scrape-companies')
def main():
    logger.info('Creating directories (to prevent race conditions in spiders)')
    data_path(HTTPCACHE_DIR, createdir=True)
    Path(IMAGES_STORE).mkdir(exist_ok=True, parents=True)

    spider_names = [
        'listed_jobs',
    ]
    logger.info(f'Scraping {spider_names}')
    scrape('juniorguru.sync.scrape_companies', spider_names)

    logger.info('Checking scrapers')
    # TODO monitoring

    logger.info('Scraping done!')
