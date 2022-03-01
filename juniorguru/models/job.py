from peewee import CharField, DateField, TextField, BooleanField, IntegerField, ForeignKeyField
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


class SubmittedJob(BaseModel):
    id = CharField(primary_key=True)
    boards_ids = JSONField(default=lambda: [], index=True)

    title = CharField()
    posted_on = DateField(index=True)
    expires_on = DateField(index=True)
    lang = CharField()

    apply_email = CharField(null=True)
    apply_url = CharField(null=True)

    company_name = CharField()
    company_url = CharField()

    locations = JSONField(null=True)
    remote = BooleanField(default=False)
    employment_types = JSONField(null=True)

    description_html = TextField()

    @classmethod
    def date_listing(cls, date_):
        return cls.select() \
            .where((cls.posted_on <= date_) &
                   (cls.expires_on >= date_))

    def to_listed(self):
        data = {field_name: getattr(self, field_name, None)
                for field_name
                in ListedJob._meta.fields.keys()
                if field_name not in ['id', 'submitted_job']}
        data['first_seen_on'] = self.posted_on
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

    locations = JSONField(null=True)
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
                if field_name not in ['id', 'submitted_job']}
        return ListedJob(**data)


class ListedJob(BaseModel):
    boards_ids = JSONField(default=lambda: [], index=True)
    submitted_job = ForeignKeyField(SubmittedJob, unique=True, null=True)

    title = CharField()
    first_seen_on = DateField(index=True)

    apply_email = CharField(null=True)
    apply_url = CharField(null=True)

    company_name = CharField()
    company_url = CharField(null=True)

    locations = JSONField(null=True)
    remote = BooleanField(default=False)
    employment_types = JSONField(null=True)
