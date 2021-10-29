import re
from datetime import date, timedelta

import arrow
from scrapy import Field, Item

from juniorguru.lib.md import md
from juniorguru.lib.repr import repr_item


class Job(Item):
    # by default set by the first pipeline, but can be overriden in the spider
    id = Field(required=True)

    # set by spiders
    posted_at = Field(required=True)
    title = Field(required=True)
    locations_raw = Field()
    remote = Field()
    company_name = Field(required=True)
    company_link = Field()
    link = Field(required=True)
    apply_link = Field()
    description_html = Field(required=True)
    employment_types = Field()
    experience_levels = Field()
    company_logo_urls = Field()

    # set by pipelines
    company_logos = Field()
    company_logo_path = Field()
    lang = Field()
    description_text = Field()
    description_sentences = Field()
    description_words = Field()
    sections = Field()  # unused atm, as well as the sections parser
    features = Field()
    junior_rank = Field()
    sort_rank = Field()
    sort_rank_components = Field()
    locations = Field()
    remote_region_raw = Field()

    def __repr__(self):
        return repr_item(self, ['title', 'link', 'apply_link', 'source'])


class JuniorGuruJob(Job):
    email = Field(required=True)
    pricing_plan = Field(required=True)
    approved_at = Field(required=True)
    expires_at = Field(required=True)


def absolute_url(url, loader_context):
    return loader_context['response'].urljoin(url)


def parse_iso_date(value):
    return arrow.get(value).date()


def parse_markdown(value):
    if value:
        return md(value.strip())


def split(string, by=','):
    if string:
        return list(filter(None, map(str.strip, string.split(by))))
    return []


def first(iterable):
    for item in iterable:
        if item is not None:
            return item
    return None


def last(iterable):
    return first(reversed(list(iterable)))


def parse_relative_date(text, today=None):
    today = today or date.today()
    if 'week' in text or 'týdn' in text:
        weeks_ago = int(re.search(r'\d+', text).group(0))
        return today - timedelta(weeks=weeks_ago)
    if 'minute' in text or 'hour' in text or 'minut' in text or 'hod' in text:
        return today
    if 'today' in text or 'dnes' in text:
        return today
    if 'yesterday' in text or 'včera' in text:
        return today - timedelta(days=1)
    if 'day' in text or 'dny' in text or 'dnem' in text:
        days_ago = int(re.search(r'\d+', text).group(0))
        return today - timedelta(days=days_ago)
    if 'month' in text or 'měs' in text:
        months_ago = int(re.search(r'\d+', text).group(0))
        return today - timedelta(days=months_ago * 30)
    raise ValueError(text)
