import gzip
from datetime import date
from pathlib import Path

from scrapy.exporters import JsonLinesItemExporter

from juniorguru.sync.scrape_jobs.settings import FEEDS


class GzipJsonLinesItemExporter(JsonLinesItemExporter):
    """
    Adds gzip compression to the standard .jsonl exporter

    Copy-pasted from https://github.com/divtiply/scrapy-gzip-exporters
    """

    def __init__(self, file, **kwargs):
        self.gzfile = gzip.GzipFile(fileobj=file, mode='wb')
        super().__init__(self.gzfile, **kwargs)

    def finish_exporting(self):
        super().finish_exporting()
        self.gzfile.close()


def uri_params(params, spider, today=None):
    """
    Used by settings.py

    https://docs.scrapy.org/en/latest/topics/feed-exports.html#feed-uri-params
    """
    today = today or date.today()
    return params | dict(year=f'{today:%Y}', month=f'{today:%m}', day=f'{today:%d}')


def feed_path(spider_name, today=None):
    """Helps to manipulate with feeds outside of the Scrapy context"""
    uri_template = list(FEEDS.keys())[0]
    params = dict(name=spider_name)
    uri_params(params, None, today)
    return Path(uri_template % params)


def feeds_dir(today=None):
    """Helps to manipulate with feeds outside of the Scrapy context"""
    return feed_path('placeholder', today).parent
