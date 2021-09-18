from peewee import CharField, DateField, TextField

from juniorguru.models.base import BaseModel, JSONField


# Experimenting with Czechitas. Calling the model 'employment' is stupid,
# but I needed to find a different name than 'job' so that the old model
# and the new model can co-exist for a while.


class Employment(BaseModel):
    title = CharField()
    company_name = CharField()
    url = CharField()
    alternative_urls = JSONField(default=lambda: [])
    description_html = TextField()
    first_seen_at = DateField()
    last_seen_at = DateField()
    source = CharField()
    source_urls = JSONField(default=lambda: [])

    @classmethod
    def get_by_item(cls, item):
        urls = set(filter(None, [item.get('url')] + item.get('alternative_urls', [])))
        alternative_urls = cls.alternative_urls.children().alias('alternative_urls')
        return cls.select() \
            .from_(cls, alternative_urls) \
            .where(cls.url.in_(urls) | alternative_urls.c.value.in_(urls)) \
            .get()

    @classmethod
    def api_listing(cls):
        return cls.select().order_by(cls.last_seen_at.desc())

    @classmethod
    def from_item(cls, item):
        return cls(id=item['id'],
                   title=item['title'],
                   company_name=item['company_name'],
                   url=item['url'],
                   alternative_urls=item['alternative_urls'],
                   description_html=item['description_html'],
                   first_seen_at=item['seen_at'],
                   last_seen_at=item['seen_at'],
                   source=item['source'],
                   source_urls=item['source_urls'])

    def merge_item(self, item):
        self.alternative_urls = list(set(self.alternative_urls + item['alternative_urls']))
        self.first_seen_at = min(self.first_seen_at, item['seen_at'])
        self.last_seen_at = max(self.last_seen_at, item['seen_at'])
        self.source_urls = list(set(self.source_urls + item['source_urls']))

    def to_api(self):
        return dict(title=self.title,
                    company_name=self.company_name,
                    url=self.url,
                    alternative_urls=self.alternative_urls,
                    first_seen_at=self.first_seen_at,
                    last_seen_at=self.last_seen_at,
                    source=self.source)
