import itertools
import re
from functools import lru_cache
from datetime import date

from peewee import CharField, DateField, ForeignKeyField, IntegerField, TextField, BooleanField

from juniorguru.models.base import BaseModel, JSONField


JOB_METRIC_NAMES = [
    'users',
    'pageviews',
    'applications',
]
JOB_IS_NEW_DAYS = 3
EMPLOYMENT_TYPES = [
    'FULL_TIME',
    'PART_TIME',
    'CONTRACT',
    'PAID_INTERNSHIP',
    'UNPAID_INTERNSHIP',
    'INTERNSHIP',
    'VOLUNTEERING',
]
EMPLOYMENT_TYPES_RULES = [
    # internship
    ({'INTERNSHIP', 'PAID_INTERNSHIP'}, {'INTERNSHIP'}),
    ({'UNPAID_INTERNSHIP', 'PAID_INTERNSHIP'}, {'INTERNSHIP'}),
    ({'INTERNSHIP', 'UNPAID_INTERNSHIP'}, {'UNPAID_INTERNSHIP'}),

    # volunteering
    ({'CONTRACT', 'VOLUNTEERING'}, {'CONTRACT'}),
    ({'PART_TIME', 'VOLUNTEERING'}, {'PART_TIME'}),
    ({'FULL_TIME', 'VOLUNTEERING'}, {'FULL_TIME'}),
    ({'INTERNSHIP', 'VOLUNTEERING'}, {'INTERNSHIP'}),
    ({'PAID_INTERNSHIP', 'VOLUNTEERING'}, {'INTERNSHIP'}),

    # full time
    ({'FULL_TIME', 'PART_TIME'}, {'FULL_TIME', 'ALSO_PART_TIME'}),
    ({'FULL_TIME', 'CONTRACT'}, {'FULL_TIME', 'ALSO_CONTRACT'}),
    ({'FULL_TIME', 'PAID_INTERNSHIP'}, {'FULL_TIME', 'ALSO_INTERNSHIP'}),
    ({'FULL_TIME', 'UNPAID_INTERNSHIP'}, {'FULL_TIME', 'ALSO_INTERNSHIP'}),
    ({'FULL_TIME', 'INTERNSHIP'}, {'FULL_TIME', 'ALSO_INTERNSHIP'}),

    # paid internship
    ({'PAID_INTERNSHIP'}, {'INTERNSHIP'}),
    ({'FULL_TIME'}, set()),
]


class Job(BaseModel):
    id = CharField(primary_key=True)
    source = CharField(index=True)
    posted_at = DateField(index=True)
    title = CharField()
    remote = BooleanField(default=False)
    location_raw = CharField(null=True)
    location_place = CharField(null=True)
    location_country = CharField(null=True)
    region = CharField(null=True)
    company_name = CharField()
    company_link = CharField(null=True)
    company_logo_path = CharField(null=True)
    employment_types = JSONField(default=lambda: [])
    link = CharField(null=True, index=True)
    lang = CharField()
    description_html = TextField()
    junior_rank = IntegerField(index=True)
    sort_rank = IntegerField(index=True)
    pricing_plan = CharField(default='community', choices=[
        ('community', None),
        ('standard', None),
        ('annual_flat_rate', None),
    ])

    # source: juniorguru
    email = CharField(null=True)
    expires_at = DateField(null=True)

    # diagnostics
    item = JSONField(null=True)
    response_url = CharField(null=True)
    response_backup_path = CharField(null=True)

    @property
    def is_highlighted(self):
        return self.pricing_plan != 'community'

    @property
    def location(self):
        if self.location_place and self.location_country == 'Česko':
            parts = [self.location_place]
        elif self.location_place and self.location_country:
            parts = [self.location_place, self.location_country]
        else:
            parts = [self.location_raw]

        if self.remote:
            parts.append('na dálku')

        parts = list(filter(None, parts))
        if parts:
            return ', '.join(parts)
        return '?'

    @property
    def metrics(self):
        result = {name: 0 for name in JOB_METRIC_NAMES}
        for metric in self.list_metrics:
            result[metric.name] = metric.value
        return result

    @property
    def newsletter_mentions(self):
        return self.list_newsletter_mentions \
            .order_by(JobNewsletterMention.sent_at.desc())

    @classmethod
    def get_by_url(cls, url):
        match = re.match(r'https?://junior.guru/jobs/([^/]+)/', url)
        if match:
            return cls.get_by_id(match.group(1))
        raise ValueError(url)

    @classmethod
    def get_by_link(cls, link):
        return cls.get(cls.link == link)

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.sort_rank.desc())

    @classmethod
    def count(cls):
        return cls.listing().count()

    @classmethod
    def companies_count(cls):
        return len(frozenset([job.company_link for job in cls.listing()]))

    @classmethod
    def juniorguru_listing(cls):
        return cls.listing().where(cls.source == 'juniorguru')

    @classmethod
    def newsletter_listing(cls, min_count, today=None):
        today = today or date.today()

        count = 0
        for item in cls.juniorguru_listing():
            yield item
            count += 1

        backfill_query = cls.listing().where(cls.source != 'juniorguru')
        yield from itertools.islice(backfill_query, min_count - count)

    def days_since_posted(self, today=None):
        today = today or date.today()
        return (today - self.posted_at).days

    def days_until_expires(self, today=None):
        today = today or date.today()
        return (self.expires_at - today).days

    def expires_soon(self, today=None):
        today = today or date.today()
        return self.days_until_expires(today=today) <= 10

    def tags(self, today=None):
        tags = []

        today = today or date.today()
        if (today - self.posted_at).days < JOB_IS_NEW_DAYS:
            tags.append('NEW')

        if self.remote:
            tags.append('REMOTE')

        employment_types = frozenset(self.employment_types)
        tags.extend(get_employment_types_tags(employment_types))

        return tags


@lru_cache()
def get_employment_types_tags(types):
    types = set(types)
    for rule_match, rule_repl in EMPLOYMENT_TYPES_RULES:
        if rule_match <= types:
            types = (types - rule_match) | rule_repl
    return types


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
    name = CharField(choices=[(name, None) for name in JOB_METRIC_NAMES])
    value = IntegerField()


class JobNewsletterMention(BaseModel):
    job = ForeignKeyField(Job, backref='list_newsletter_mentions')
    sent_at = DateField()
    link = CharField()
