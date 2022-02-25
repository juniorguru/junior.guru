from peewee import BooleanField, CharField, DateField, TextField, IntegerField

from juniorguru.models.base import BaseModel, JSONField


# Experimenting with Czechitas. Calling the model 'employment' is stupid,
# but I needed to find a different name than 'job' so that the old model
# and the new model can co-exist for a while.


class Employment(BaseModel):
    class Meta:
        table_name = 'employment_v1'

    ############################################################################
    ##                                                                        ##
    ##  BIG FAT WARNING:                                                      ##
    ##                                                                        ##
    ##  When changing this model, you MUST update also the 'backups' scraper  ##
    ##  so that it counts with the changes. If you change the model           ##
    ##  significantly, please do raise the version number above and create    ##
    ##  a completely new adapter in the 'backups' scraper.                    ##
    ##                                                                        ##
    ############################################################################

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

    # juniority
    juniority_re_score = IntegerField(null=True)
    juniority_ai_opinion = BooleanField(null=True)
    juniority_votes_score = IntegerField(default=0)
    juniority_votes_count = IntegerField(default=0)

    # meta information
    source = CharField()
    source_urls = JSONField(default=lambda: [])
    build_url = CharField(null=True)
    items_merged_count = IntegerField(default=0)

    @classmethod
    def get_by_item(cls, item):
        return cls.select() \
            .where(cls.url == item['url']) \
            .get()

    @classmethod
    def get_by_url(cls, url):
        return cls.select() \
            .where(cls.url == url) \
            .get()

    @classmethod
    def loaded_from_backups_count(cls):
        return cls.select() \
            .where(cls.build_url.is_null(False)) \
            .count()

    @classmethod
    def api_listing(cls):
        return cls.select() \
            .where((cls.juniority_re_score > 0) | (cls.source == 'juniorguru')) \
            .order_by(cls.last_seen_at.desc(), cls.first_seen_at.desc())

    @classmethod
    def from_item(cls, item):
        return cls(**{field_name: item.get(field_name)
                   for field_name in cls._meta.fields.keys()
                   if field_name in item})

    def to_api(self):
        return dict(**dict(
                        title=self.title,
                        company_name=self.company_name,
                        url=self.url,
                        remote=self.remote,
                        first_seen_at=self.first_seen_at,
                        last_seen_at=self.last_seen_at,
                        lang=self.lang,
                        juniority_score=self.juniority_re_score,
                        source=self.source,
                    ),
                    **{
                        f'external_ids_{i}': value for i, value
                        in columns(self.external_ids, 10)
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

    def merge_item(self, item):
        for field_name in self.__class__._meta.fields.keys():
            try:
                # use merging method if present
                merge_method = getattr(self, f'_merge_{field_name}')
                setattr(self, field_name, merge_method(item))
            except AttributeError:
                # overwrite with newer data
                if item['last_seen_at'] >= self.last_seen_at:
                    old_value = getattr(self, field_name)
                    new_value = item.get(field_name, old_value)
                    setattr(self, field_name, new_value)

    def _merge_external_ids(self, item):
        return list(set(self.external_ids + item.get('external_ids', [])))

    def _merge_source_urls(self, item):
        return list(set(self.source_urls + item.get('source_urls', [])))

    def _merge_first_seen_at(self, item):
        return min(self.first_seen_at, item['first_seen_at'])

    def _merge_last_seen_at(self, item):
        return max(self.last_seen_at, item['last_seen_at'])

    def _merge_items_merged_count(self, item):
        return self.items_merged_count + 1


def columns(values, columns_count):
    values = list(values or [])
    values_count = len(values)
    return enumerate([values[i] if values_count > i else None for i in range(columns_count)])
