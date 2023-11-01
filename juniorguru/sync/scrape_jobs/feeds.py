import gzip
from datetime import date
from pathlib import Path

from scrapy import Spider
from scrapy.exporters import JsonLinesItemExporter

from juniorguru.sync.scrape_jobs.settings import FEEDS


class GzipJsonLinesItemExporter(JsonLinesItemExporter):
    """
    Adds gzip compression to the standard .jsonl exporter

    Copy-pasted from https://github.com/divtiply/scrapy-gzip-exporters
    """

    def __init__(self, file, **kwargs):
        self.gzfile = gzip.GzipFile(fileobj=file, mode="wb")
        super().__init__(self.gzfile, **kwargs)

    def finish_exporting(self):
        super().finish_exporting()
        self.gzfile.close()


def uri_params(params: dict, spider: Spider, today: date = None) -> dict[str, str]:
    """
    Used by settings.py

    https://docs.scrapy.org/en/latest/topics/feed-exports.html#feed-uri-params
    """
    today = today or date.today()
    return {
        **params,
        "year": f"{today:%Y}",
        "month": f"{today:%m}",
        "day": f"{today:%d}",
    }


def get_feed_path(spider_name: str, today: date = None) -> Path:
    """Helps to manipulate with feeds outside of the Scrapy context"""
    uri_template = list(FEEDS.keys())[0]
    params = uri_params(dict(name=spider_name), None, today)
    return Path(uri_template % params)


def get_feeds_dir(today: date = None) -> Path:
    """Helps to manipulate with feeds outside of the Scrapy context"""
    return get_feed_path("placeholder", today).parent
