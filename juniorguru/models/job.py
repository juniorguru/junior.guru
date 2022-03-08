from functools import lru_cache
from datetime import date, datetime, time

from peewee import fn, Expression, CharField, DateField, TextField, BooleanField, IntegerField, ForeignKeyField
from playhouse.shortcuts import model_to_dict

from juniorguru.models.base import BaseModel, JSONField


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

JOB_NEW_DAYS = 3

JOB_EXPIRED_SOON_DAYS = 10


class SubmittedJob(BaseModel):
    id = CharField(primary_key=True)
    boards_ids = JSONField(default=lambda: [], index=True)

    title = CharField()
    posted_on = DateField(index=True)
    expires_on = DateField(index=True)
    lang = CharField()

    url = CharField(unique=True)
    apply_email = CharField(null=True)
    apply_url = CharField(null=True)

    company_name = CharField()
    company_url = CharField()
    company_logo_urls = JSONField(default=lambda: [])

    locations_raw = JSONField(null=True)
    remote = BooleanField(default=False)
    employment_types = JSONField(null=True)

    description_html = TextField()

    def days_since_posted(self, today=None):
        today = today or date.today()
        return (today - self.posted_on).days

    def days_until_expires(self, today=None):
        today = today or date.today()
        return (self.expires_on - today).days

    def expires_soon(self, today=None):
        today = today or date.today()
        return self.days_until_expires(today=today) <= JOB_EXPIRED_SOON_DAYS

    @classmethod
    def date_listing(cls, date_):
        return cls.select() \
            .where((cls.posted_on <= date_) &
                   (cls.expires_on >= date_))

    def to_listed(self):
        data = {field_name: getattr(self, field_name, None)
                for field_name
                in ListedJob._meta.fields.keys()
                if (field_name in self.__class__._meta.fields and
                    field_name not in ['id', 'submitted_job'])}
        data['first_seen_on'] = self.posted_on
        data['submitted_job'] = self
        return ListedJob(**data)


class ScrapedJob(BaseModel):
    boards_ids = JSONField(default=lambda: [], index=True)

    title = CharField()
    first_seen_on = DateField(index=True)
    last_seen_on = DateField(index=True)
    lang = CharField(null=True)

    url = CharField(unique=True)
    apply_url = CharField(null=True)

    company_name = CharField()
    company_url = CharField(null=True)
    company_logo_urls = JSONField(default=lambda: [])

    locations_raw = JSONField(null=True)
    remote = BooleanField(default=False)
    employment_types = JSONField(null=True)

    description_html = TextField()
    features = JSONField(default=lambda: [])
    juniority_re_score = IntegerField(null=True)
    juniority_ai_opinion = BooleanField(null=True)
    juniority_votes_score = IntegerField(default=0)
    juniority_votes_count = IntegerField(default=0)

    source = CharField()
    source_urls = JSONField(default=lambda: [])

    @classmethod
    def date_listing(cls, date_, min_juniority_re_score=0):
        return cls.select() \
            .where((cls.last_seen_on == date_) &
                   (cls.juniority_re_score >= min_juniority_re_score))

    @classmethod
    def latest_seen_on(cls):
        job = cls.select() \
            .order_by(cls.last_seen_on.desc()) \
            .first()
        return job.last_seen_on if job else None

    @classmethod
    def get_by_item(cls, item):
        return cls.select() \
            .where(cls.url == item['url']) \
            .get()

    @classmethod
    def from_item(cls, item):
        data = {field_name: item.get(field_name)
                for field_name in cls._meta.fields.keys()
                if field_name in item}
        return cls(**data)

    def to_item(self):
        return model_to_dict(self)

    def merge_item(self, item):
        for field_name in self.__class__._meta.fields.keys():
            try:
                # use merging method if present
                merge_method = getattr(self, f'_merge_{field_name}')
                setattr(self, field_name, merge_method(item))
            except AttributeError:
                # overwrite with newer data
                if item['last_seen_on'] >= self.last_seen_on:
                    old_value = getattr(self, field_name)
                    new_value = item.get(field_name, old_value)
                    setattr(self, field_name, new_value)

    def _merge_boards_ids(self, item):
        return list(set(self.boards_ids + item.get('boards_ids', [])))

    def _merge_items_hashes(self, item):
        return list(set(self.items_hashes + item.get('items_hashes', [])))

    def _merge_source_urls(self, item):
        return list(set(self.source_urls + item.get('source_urls', [])))

    def _merge_first_seen_on(self, item):
        return min(self.first_seen_on, item['first_seen_on'])

    def _merge_last_seen_on(self, item):
        return max(self.last_seen_on, item['last_seen_on'])

    def _merge_items_merged_count(self, item):
        return self.items_merged_count + 1

    def to_listed(self):
        data = {field_name: getattr(self, field_name, None)
                for field_name
                in ListedJob._meta.fields.keys()
                if (field_name in self.__class__._meta.fields and
                    field_name not in ['id', 'submitted_job'])}
        return ListedJob(**data)


class ListedJob(BaseModel):
    boards_ids = JSONField(default=lambda: [], index=True)
    submitted_job = ForeignKeyField(SubmittedJob, unique=True, null=True)

    title = CharField()
    first_seen_on = DateField(index=True)
    lang = CharField()

    url = CharField()
    apply_email = CharField(null=True)
    apply_url = CharField(null=True)

    company_name = CharField()
    company_url = CharField(null=True)
    company_logo_urls = JSONField(default=lambda: [])
    company_logo_path = CharField(null=True)

    locations_raw = JSONField(null=True)
    locations = JSONField(null=True)
    remote = BooleanField(default=False)
    employment_types = JSONField(null=True)

    @property
    def effective_url(self):
        if self.is_submitted:
            return self.url
        return self.apply_url or self.url

    @property
    def is_submitted(self):
        return bool(self.submitted_job)

    @property
    def is_highlighted(self):
        return self.is_submitted

    def tags(self, today=None):
        tags = []

        today = today or date.today()
        if (today - self.first_seen_on).days < JOB_NEW_DAYS:
            tags.append('NEW')

        if self.remote:
            tags.append('REMOTE')

        employment_types = frozenset(self.employment_types)
        tags.extend(get_employment_types_tags(employment_types))

        return tags

    @property
    def location(self):
        # TODO refactor, this is terrible
        locations = self.locations or []
        if len(locations) == 1:
            location = locations[0]
            name, region = location['name'], location['region']
            parts = [name] if name == region else [name, region]
            if self.remote:
                parts.append('na dálku')
            parts = list(filter(None, parts))
            if parts:
                return ', '.join(parts)
            return '?'
        else:
            parts = list(sorted(filter(None, [loc['name'] for loc in locations])))
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

    @classmethod
    def count(cls):
        return cls.listing().count()

    @classmethod
    def listing(cls, today=None):
        today = today or date.today()
        days_since_first_seen = fn.julianday(today) - fn.julianday(cls.first_seen_on)
        return cls.select() \
            .order_by(cls.submitted_job.is_null(),
                      Expression(days_since_first_seen, '%', 30))

    @classmethod
    def favicon_listing(cls):
        return cls.select() \
            .where(cls.company_logo_path.is_null() &
                   cls.company_url.is_null(False))

    @classmethod
    def submitted_listing(cls):
        return cls.select() \
            .where(cls.submitted_job.is_null(False))

    @classmethod
    def get_by_submitted_id(cls, submitted_job_id):
        return cls.select() \
            .where(cls.submitted_job == submitted_job_id) \
            .get()

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

    @classmethod
    def api_listing(cls):
        return cls.select() \
            .order_by(cls.first_seen_on.desc())

    def to_api(self):
        return dict(**dict(
                        title=self.title,
                        company_name=self.company_name,
                        url=self.effective_url,
                        remote=self.remote,
                        first_seen_at=datetime.combine(self.first_seen_on, time(0, 0)),  # datetime for backwards compatibility
                        last_seen_at=None,  # not relevant anymore, equals to present moment
                        lang=self.lang,
                        juniority_score=None,  # won't expose publicly anymore
                        source=None,  # use external IDs instead
                    ),
                    **{
                        f'external_ids_{i}': value for i, value  # renamed elsewhere, but keeping backwards compatible
                        in columns(self.boards_ids, 10)
                    },
                    **{
                        f'locations_{i}_name': (value['name'] if value else None) for i, value
                        in columns(self.locations, 20)
                    },
                    **{
                        f'locations_{i}_region': (value['region'] if value else None) for i, value
                        in columns(self.locations, 20)
                    },
                    **{
                        f'employment_types_{i}': value for i, value
                        in columns(self.employment_types, 10)
                    })


@lru_cache()
def get_employment_types_tags(types):
    types = set(types)
    for rule_match, rule_repl in EMPLOYMENT_TYPES_RULES:
        if rule_match <= types:
            types = (types - rule_match) | rule_repl
    return types


def columns(values, columns_count):
    values = list(values or [])
    values_count = len(values)
    return enumerate([values[i] if values_count > i else None for i in range(columns_count)])
