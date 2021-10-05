import importlib

from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from juniorguru.lib import loggers


logger = loggers.get(__name__)


def scrape(scrapy_project_package, spider_names):
    settings_module_name = f'{scrapy_project_package}.settings'
    logger.info(f'Importing Scrapy settings: {settings_module_name}')
    settings = Settings()
    settings.setmodule(settings_module_name, priority='project')

    logger.info(f"Preparing to crawl: {', '.join(spider_names)}")
    crawler = CrawlerProcess(settings=settings, install_root_handler=False)
    for spider_name in spider_names:
        spider_module_name = f'{scrapy_project_package}.spiders.{spider_name}'
        spider = importlib.import_module(spider_module_name)
        crawler.crawl(spider.Spider)

    logger.info('Starting the crawler')
    crawler.start()
    logger.info('Crawling finished')
