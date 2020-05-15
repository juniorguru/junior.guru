import re
from datetime import datetime, timedelta

from scrapy import Field, Item


class Job(Item):
    posted_at = Field(required=True)
    title = Field(required=True)
    location = Field(required=True)
    company_name = Field(required=True)
    company_link = Field()
    link = Field(required=True)
    description_raw = Field(required=True)
    lang = Field()
    # sections = Field()
    contents = Field()
    features = Field()
    employment_types = Field()
    experience_levels = Field()


def absolute_url(url, loader_context):
    return loader_context['response'].urljoin(url)


def split(string, by=','):
    if string:
        return list(filter(None, map(str.strip, string.split(by))))
    return []


def first(iterable):
    try:
        return iterable[0]
    except IndexError:
        return None


def parse_relative_time(text, now=None):
    now = now or datetime.utcnow()
    if 'week' in text:
        weeks_ago = int(re.search(r'\d+', text).group(0))
        return now - timedelta(weeks=weeks_ago)
    if 'minute' in text or 'hour' in text:
        return now
    if 'yesterday' in text:
        return now - timedelta(days=1)
    if 'day' in text:
        days_ago = int(re.search(r'\d+', text).group(0))
        return now - timedelta(days=days_ago)
    if 'month' in text:
        months_ago = int(re.search(r'\d+', text).group(0))
        return now - timedelta(days=months_ago * 30)
    raise ValueError(text)
