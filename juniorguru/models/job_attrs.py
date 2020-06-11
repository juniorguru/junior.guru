import itertools
import re
from datetime import date

from juniorguru.models.metrics import JOB_METRIC_NAMES, JobMetric


# This file exists because of circular dependencies between Job and JobMetric
# https://stackoverflow.com/q/62327182/325365
#
# The workaround works like this: The stuff listed in __all__ gets implicitly
# attached to the Job model as attributes in the __init__.py
# of the models package.


__all__ = ['get_by_url', 'get_by_link', 'listing', 'newsletter_listing',
           'juniorguru_listing', 'bot_listing', 'scraped_listing', 'count',
           'companies_count', 'metrics']


@classmethod
def get_by_url(cls, url):
    match = re.match(r'https?://junior.guru/jobs/([^/]+)/', url)
    if match:
        return cls.get_by_id(match.group(1))
    raise ValueError(url)


@classmethod
def get_by_link(cls, url):
    return cls.get(cls.link == url)


@classmethod
def listing(cls):
    return cls.juniorguru_listing()


@classmethod
def newsletter_listing(cls, min_count, today=None):
    today = today or date.today()

    count = 0
    query = cls.select() \
        .where((cls.source == 'juniorguru') &
                (cls.approved_at.is_null(False)) &
                (cls.is_sent == False) &
                (cls.expired_at.is_null() | (cls.expired_at > today))) \
        .order_by(cls.posted_at)
    for item in query:
        yield item
        count += 1

    backfill_query = cls.select() \
        .where(cls.source != 'juniorguru', cls.jg_rank > 0) \
        .order_by(cls.jg_rank.desc(), cls.posted_at.desc())
    yield from itertools.islice(backfill_query, min_count - count)


@classmethod
def juniorguru_listing(cls, today=None):
    today = today or date.today()
    return cls.select() \
        .where((cls.source == 'juniorguru') &
                (cls.approved_at.is_null(False)) &
                (cls.expired_at.is_null() | (cls.expired_at > today))) \
        .order_by(cls.posted_at.desc())


@classmethod
def bot_listing(cls):
    return cls.select() \
        .where(cls.source != 'juniorguru',
                cls.jg_rank > 0) \
        .order_by(cls.jg_rank.desc(), cls.posted_at.desc())


@classmethod
def scraped_listing(cls):
    return cls.select(cls, JobMetric) \
        .join(JobMetric) \
        .where(cls.source != 'juniorguru') \
        .order_by(cls.jg_rank.desc(), cls.posted_at.desc())


@classmethod
def count(cls):
    return cls.listing().count()


@classmethod
def companies_count(cls):
    return len(frozenset([job.company_link for job in cls.listing()]))


@property
def metrics(self):  # _metrics is a JobMetric backref
    result = {name: 0 for name in JOB_METRIC_NAMES}
    for metric in self._metrics:
        result[metric.name] = metric.value
    return result
