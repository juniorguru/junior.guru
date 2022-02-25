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
    locations = JSONField(default=lambda: [])
    company_name = CharField()
    company_link = CharField(null=True)
    company_logo_path = CharField(null=True)
    employment_types = JSONField(default=lambda: [])
    link = CharField(index=True)
    apply_link = CharField(null=True)
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
    def is_juniorguru(self):
        return self.source == 'juniorguru'

    @property
    def is_highlighted(self):
        return self.pricing_plan != 'community'

    @property
    def effective_link(self):
        if self.is_juniorguru:
            return self.link
        return self.apply_link or self.link

    @property
    def location(self):
        # TODO refactor, this is terrible
        if len(self.locations) == 1:
            location = self.locations[0]
            name, region = location['name'], location['region']
            parts = [name] if name == region else [name, region]
            if self.remote:
                parts.append('na dálku')
            parts = list(filter(None, parts))
            if parts:
                return ', '.join(parts)
            return '?'
        else:
            parts = list(sorted(filter(None, [loc['name'] for loc in self.locations])))
            if len(parts) > 2:
                parts = parts[:2]
                if self.remote:
                    parts[-1] += ' a další'
                    parts.append('na dálku')
                    return ', '.join(parts)
                else:
                    return ', '.join(parts) + '…'
            elif parts:
                return ', '.join(parts + (['na dálku'] if self.remote else []))
            if self.remote:
                return 'na dálku'
            return '?'

    @property
    def metrics(self):
        result = {name: 0 for name in JOB_METRIC_NAMES}
        for metric in self.list_metrics:
            result[metric.name] = metric.value
        return result

    @classmethod
    def get_by_url(cls, url):
        match = re.match(r'https?://junior.guru/jobs/([^/]+)/', url)
        if match:
            return cls.get_by_id(match.group(1))
        return cls.select() \
            .where((cls.link == url) | (cls.apply_link == url)) \
            .get()

    @classmethod
    def juniorguru_get_by_id(cls, id):
        return cls.juniorguru_listing().where(cls.id == id).get()

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.sort_rank.desc())

    @classmethod
    def aggregate_metrics(cls):
        approved_jobs_count = cls.listing() \
            .where(cls.source != 'juniorguru') \
            .count()
        companies_count = len(JobDropped.expired_company_links() |
                              {job.company_link for job in cls.juniorguru_listing()})
        return dict(companies_count=companies_count,
                    jobs_count=cls.listing().count(),
                    approved_jobs_count=approved_jobs_count,
                    rejected_jobs_count=JobDropped.rejected_count())

    @classmethod
    def juniorguru_listing(cls):
        return cls.listing().where(cls.source == 'juniorguru')

    @classmethod
    def region_listing(cls, region):
        locations = cls.locations.tree().alias('locations')
        return cls.listing() \
            .from_(cls, locations) \
            .where((locations.c.key == 'region') &
                   (locations.c.value == region))

    @classmethod
    def remote_listing(cls):
        return cls.listing().where(cls.remote == True)

    @classmethod
    def tags_listing(cls, tags):
        tags = set(tags)
        return [job for job in cls.listing() if tags & set(job.tags())]

    @classmethod
    def internship_listing(cls):
        return cls.tags_listing([
            'INTERNSHIP',
            'UNPAID_INTERNSHIP',
            'ALSO_INTERNSHIP',
        ])

    @classmethod
    def volunteering_listing(cls):
        return cls.tags_listing(['VOLUNTEERING'])

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
    source = CharField()
    response_url = CharField()
    response_backup_path = CharField(null=True)
    item = JSONField()

    @classmethod
    def admin_listing(cls, types=None):
        jobs = cls.select()
        if types:
            jobs = jobs.where(cls.type.in_(types))
        return sorted(jobs, key=lambda job: (
            job.type,
            'junior' not in job.item.get('title', '').lower(),
            -1 * job.item.get('junior_rank', -1000),
            job.reason,
        ))

    @classmethod
    def rejected_count(cls):
        return cls.select() \
            .where(cls.source != 'juniorguru') \
            .count()

    @classmethod
    def sources(cls):
        return {job_dropped.source for job_dropped in JobDropped.select()}

    @classmethod
    def expired_company_links(cls):
        return {job_dropped.item.get('company_link') for job_dropped
                in cls.select().where(JobDropped.type == 'Expired')}


class JobError(BaseModel):
    message = CharField()
    trace = CharField()
    signal = CharField(choices=(('item', None), ('spider', None)))
    source = CharField()
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
