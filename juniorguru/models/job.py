import itertools
from datetime import date

from peewee import (BooleanField, CharField, DateField,
                    DateTimeField, IntegerField)

from juniorguru.models.base import BaseModel, JSONField


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
    link = CharField(null=True)  # required for scraped
    source = CharField()

    # only set by JG
    email = CharField(null=True)  # required for JG
    description = CharField(null=True)  # required for JG
    approved_at = DateField(null=True)
    expired_at = DateField(null=True)
    is_sent = BooleanField(default=False)

    # only set by scraped
    lang = CharField(null=True)  # required for scraped
    jg_rank = IntegerField(null=True)  # required for scraped
    response_url = CharField(null=True)  # required for scraped
    response_backup_path = CharField(null=True)
    item = JSONField(null=True)  # required for scraped

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
        return cls.select() \
            .where(cls.source != 'juniorguru') \
            .order_by(cls.jg_rank.desc(), cls.posted_at.desc())

    @classmethod
    def count(cls):
        return cls.listing().count()

    @classmethod
    def companies_count(cls):
        return len(frozenset([job.company_link for job in cls.listing()]))


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
