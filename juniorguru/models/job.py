import itertools
import re
from datetime import date

from peewee import (CharField, DateField, DateTimeField,
                    ForeignKeyField, IntegerField, TextField)

from juniorguru.models.base import BaseModel, JSONField
from juniorguru.url_params import set_params


JOB_METRIC_NAMES = [
    'users',
    'pageviews',
    'applications',
]


class UniqueSortedListField(CharField):
    def db_value(self, python_value):
        assert all(';' not in item for item in python_value)
        return ';'.join(self._sort(frozenset(python_value)))

    def python_value(self, db_value):
        return db_value.split(';')

    def _sort(self, iterable):
        return sorted(iterable)


class EmploymentTypeField(UniqueSortedListField):
    known_types_sorted = [
        'full-time',
        'part-time',
        'contract',
        'paid internship',
        'unpaid internship',
        'internship',
        'volunteering',
    ]

    def _key(self, item):
        if item in self.known_types_sorted:
            return (self.known_types_sorted.index(item), '')
        return (1000, item)

    def _sort(self, iterable):
        return sorted(iterable, key=self._key)


class Job(BaseModel):
    id = CharField(primary_key=True)
    posted_at = DateTimeField(index=True)
    title = CharField()
    location = CharField()
    company_name = CharField()
    company_link = CharField(null=True)  # required for JG
    employment_types = EmploymentTypeField()
    link = CharField(null=True, index=True)  # required for scraped
    source = CharField()

    # only set by JG
    email = CharField(null=True)  # required for JG
    description = TextField(null=True)  # required for JG
    pricing_plan = CharField(default='community', choices=[
        ('community', None),
        ('standard', None),
    ])
    approved_at = DateField(null=True)
    expires_at = DateField(null=True)
    newsletter_at = DateField(null=True)

    # only set by scraped
    lang = CharField(null=True)  # required for scraped
    jg_rank = IntegerField(null=True)  # required for scraped
    response_url = CharField(null=True)  # required for scraped
    response_backup_path = CharField(null=True)
    item = JSONField(null=True)  # required for scraped

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


class JobDropped(BaseModel):
    type = CharField()
    reason = CharField()
    response_url = CharField()
    response_backup_path = CharField(null=True)
    item = JSONField()

    @classmethod
    def admin_listing(cls):
        return cls.select().order_by(cls.type, cls.reason)


class JobError(BaseModel):
    message = CharField()
    trace = CharField()
    signal = CharField(choices=(('item', None), ('spider', None)))
    spider = CharField()
    response_url = CharField()
    response_backup_path = CharField(null=True)
    item = JSONField(null=True)

    @classmethod
    def admin_listing(cls):
        return cls.select().order_by(cls.message)


class JobMetric(BaseModel):
    job = ForeignKeyField(Job, backref='list_metrics')
    name = CharField(choices=[(n, None) for n in JOB_METRIC_NAMES])
    value = IntegerField()
