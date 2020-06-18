import itertools
import re
from datetime import date

from juniorguru.models.metrics import JOB_METRIC_NAMES, JobMetric
from juniorguru.url_params import set_params


# This file exists because of circular dependencies between Job and JobMetric
# https://stackoverflow.com/q/62327182/325365
#
# The workaround works like this: The stuff listed in __all__ gets implicitly
# attached to the Job model as attributes in the __init__.py
# of the models package.


__all__ = ['get_by_url', 'get_by_link', 'listing', 'newsletter_listing',
           'juniorguru_listing', 'bot_listing', 'scraped_listing', 'count',
           'companies_count', 'metrics', 'effective_approved_at', 'juniorguru',
           'link_utm']


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
               cls.approved_at.is_null(False) &
               cls.newsletter_at.is_null() &
               (cls.expires_at.is_null() | (cls.expires_at > today))) \
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
    return cls.juniorguru() \
        .where(cls.approved_at.is_null(False) &
               (cls.expires_at.is_null() | (cls.expires_at > today)))


@classmethod
def juniorguru(cls):
    return cls.select() \
        .where(cls.source == 'juniorguru') \
        .order_by(cls.posted_at.desc())


@classmethod
def bot_listing(cls):
    return cls.select() \
        .where(cls.source != 'juniorguru',
                cls.jg_rank > 0) \
        .order_by(cls.jg_rank.desc(), cls.posted_at.desc())


@classmethod
def scraped_listing(cls):
    return cls.select() \
        .where(cls.source != 'juniorguru') \
        .order_by(cls.jg_rank.desc(), cls.posted_at.desc())


@classmethod
def count(cls):
    return cls.listing().count()


@classmethod
def companies_count(cls):
    return len(frozenset([job.company_link for job in cls.listing()]))


@property
def metrics(self):
    result = {name: 0 for name in JOB_METRIC_NAMES}
    for metric in self.list_metrics:  # JobMetric backref
        result[metric.name] = metric.value
    return result


@property
def effective_approved_at(self):
    # before 2020-06-04 the approved field was only a boolean, so using
    # 'posted_at' instead for anything approved that date or before
    if self.approved_at <= date(2020, 6, 4):
        return self.posted_at.date()
    return self.approved_at


@property
def link_utm(self):
    if re.search(r'[\?\&]utm_[a-z]+', self.link):
        return self.link
    return set_params(self.link, {
        'utm_source': 'juniorguru',
        'utm_medium': 'job_board',
        'utm_campaign': 'juniorguru',
    })
