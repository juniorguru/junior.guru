from peewee import CharField, DateField, IntegerField, TextField, BooleanField

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


class Job(BaseModel):
    title = CharField()
    company_name = CharField()
    url = CharField(unique=True)
    apply_url = CharField(null=True)
    external_ids = JSONField(default=lambda: [])
    locations = JSONField(null=True)
    remote = BooleanField(default=False)
    lang = CharField(null=True)
    description_html = TextField()
    description_text = TextField()
    first_seen_at = DateField()
    last_seen_at = DateField()
    employment_types = JSONField(null=True)

    # meta information
    source = CharField()
    source_urls = JSONField(default=lambda: [])
    items_merged_count = IntegerField(default=0)
