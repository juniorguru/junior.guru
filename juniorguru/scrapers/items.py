import re
from datetime import date, timedelta

from scrapy import Field, Item


class Job(Item):
    # set by spiders
    posted_at = Field(required=True)
    title = Field(required=True)
    location = Field(required=True)
    company_name = Field(required=True)
    company_link = Field()
    link = Field(required=True)
    description_html = Field(required=True)
    employment_types = Field()
    experience_levels = Field()

    # set by pipelines
    lang = Field()
    description_text = Field()
    description_sentences = Field()
    description_words = Field()
    sections = Field()  # unused atm, as well as the sections parser
    features = Field()
    jg_rank = Field()


class JuniorGuruJob(Job):
    id = Field(required=True)
    link = Field()
    email = Field(required=True)
    pricing_plan = Field(required=True)
    approved_at = Field(required=True)
    expires_at = Field(required=True)


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


def parse_relative_time(text, today=None):
    today = today or date.today()
    if 'week' in text:
        weeks_ago = int(re.search(r'\d+', text).group(0))
        return today - timedelta(weeks=weeks_ago)
    if 'minute' in text or 'hour' in text:
        return today
    if 'yesterday' in text:
        return today - timedelta(days=1)
    if 'day' in text:
        days_ago = int(re.search(r'\d+', text).group(0))
        return today - timedelta(days=days_ago)
    if 'month' in text:
        months_ago = int(re.search(r'\d+', text).group(0))
        return today - timedelta(days=months_ago * 30)
    raise ValueError(text)
