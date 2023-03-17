import importlib
from multiprocessing import Process

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


def scrape(*args, **kwargs):
    logger.debug('Starting the Twisted reactor process')
    process = Process(target=run_twisted_reactor, args=args, kwargs=kwargs)
    process.start()
    logger.debug('Waiting for the Twisted reactor process to finish')
    process.join()
    logger.debug('Twisted reactor process done')
    if process.exitcode != 0:
        raise RuntimeError(f'Twisted reactor process finished with non-zero exit code: {process.exitcode}')


def run_twisted_reactor(scrapy_project_package, spider_names):
    # use asyncio? https://docs.scrapy.org/en/latest/topics/asyncio.html#using-asyncio
    settings_module_name = f'{scrapy_project_package}.settings'
    logger.debug(f'Importing Scrapy settings: {settings_module_name}')
    settings = Settings()
    settings.setmodule(settings_module_name, priority='project')

    logger.debug(f"Preparing to crawl: {', '.join(spider_names)}")
    crawler = CrawlerProcess(settings=settings, install_root_handler=False)
    for spider_name in spider_names:
        spider_module_name = f'{scrapy_project_package}.spiders.{spider_name}'
        spider = importlib.import_module(spider_module_name)
        crawler.crawl(spider.Spider)

    logger.debug('Starting the crawler')
    crawler.start()
    logger.debug('Crawling finished')
