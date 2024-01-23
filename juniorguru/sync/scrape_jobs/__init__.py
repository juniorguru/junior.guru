import math

from scrapy.utils.project import data_path

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.scrapers import scrape
from juniorguru.sync.scrape_jobs.feeds import get_feed_path, get_feeds_dir
from juniorguru.sync.scrape_jobs.settings import HTTPCACHE_DIR


logger = loggers.from_path(__file__)


class JobsScrapingException(Exception):
    pass


@cli.sync_command()
def main():
    feeds_dir = get_feeds_dir()
    spider_names = [
        "linkedin",
        "startupjobs",
        "remoteok",
        "weworkremotely",
        "jobscz",
    ]

    logger.info("Creating directories to prevent race conditions in spiders")
    data_path(HTTPCACHE_DIR, createdir=True)
    feeds_dir.mkdir(exist_ok=True, parents=True)

    logger.info("Figuring out what to scrape")
    feeds = [
        {
            "file_name": feed_path.name,
            "spider_name": feed_path.name.removesuffix(".jsonl.gz"),
            "size_kb": math.ceil(feed_path.stat().st_size / 1000),
        }
        for feed_path in feeds_dir.glob("*.jsonl.gz")
    ]
    for feed in feeds:
        logger.info(f'Already scraped today: {feed["file_name"]}, {feed["size_kb"]}kB')
    spider_names = sorted(
        set(spider_names) - set(feed["spider_name"] for feed in feeds)
    )

    if spider_names:
        logger.info(f"Scraping {spider_names}")
        scrape("juniorguru.sync.scrape_jobs", spider_names)

        logger.info("Checking scrapers")
        # TODO vcucnout scripts/check_scrapers.py
        for spider_name in spider_names:
            path = get_feed_path(spider_name)
            if not path:
                raise JobsScrapingException(
                    f"Scraper {spider_name} didn't save any items"
                )
            if not path.stat().st_size:
                raise JobsScrapingException(
                    f"Scraper {spider_name} didn't save any items"
                )

        logger.info("Scraping done!")
    else:
        logger.info("Nothing to scrape!")
