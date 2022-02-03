from pathlib import Path
from datetime import date

from juniorguru.jobs.settings import FEEDS


def uri_params(params, spider, today=None):
    """
    Used from settings

    https://docs.scrapy.org/en/latest/topics/feed-exports.html#feed-uri-params
    """
    today = today or date.today()
    params['year'] = f'{today:%Y}'
    params['month'] = f'{today:%m}'
    params['day'] = f'{today:%d}'


def feed_path(spider_name, today=None):
    """Helps to manipulate with feeds outside of the Scrapy context"""
    uri_template = list(FEEDS.keys())[0]
    params = dict(name=spider_name)
    uri_params(params, None, today)
    return Path(uri_template % params)


def feeds_dir(today=None):
    """Helps to manipulate with feeds outside of the Scrapy context"""
    return feed_path('placeholder', today).parent
