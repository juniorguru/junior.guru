from peewee import CharField, DateField, TextField, BooleanField

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
    first_seen_on = DateField(index=True)
    last_seen_on = DateField(index=True)
    lang = CharField(null=True)
    external_ids = JSONField(default=lambda: [], index=True)

    url = CharField(unique=True)
    apply_url = CharField(null=True)

    company_name = CharField()
    company_url = CharField(null=True)

    locations = JSONField(null=True)
    remote = BooleanField(default=False)
    employment_types = JSONField(null=True)

    description_html = TextField()

    source = CharField()
    source_urls = JSONField(default=lambda: [])

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

    def _merge_external_ids(self, item):
        return list(set(self.external_ids + item.get('external_ids', [])))

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
