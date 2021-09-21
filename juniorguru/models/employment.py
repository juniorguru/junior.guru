from peewee import CharField, DateField, TextField, IntegerField

from juniorguru.models.base import BaseModel, JSONField


# Experimenting with Czechitas. Calling the model 'employment' is stupid,
# but I needed to find a different name than 'job' so that the old model
# and the new model can co-exist for a while.


class Employment(BaseModel):
    title = CharField()
    company_name = CharField()
    urls = JSONField(unique=True)
    locations = JSONField(null=True)
    lang = CharField(null=True)
    description_html = TextField()
    first_seen_at = DateField()
    last_seen_at = DateField()
    source = CharField()
    source_urls = JSONField(default=lambda: [])
    items_merged_count = IntegerField(default=0)

    @classmethod
    def get_by_item(cls, item):
        urls = cls.urls.children().alias('urls')
        return cls.select() \
            .from_(cls, urls) \
            .where(urls.c.value.in_(item['urls'])) \
            .get()

    @classmethod
    def api_listing(cls):
        return cls.select().order_by(cls.last_seen_at.desc())

    @classmethod
    def from_item(cls, item):
        return cls(title=item['title'],
                   company_name=item['company_name'],
                   urls=item['urls'],
                   locations=item['locations'],
                   description_html=item['description_html'],
                   lang=item.get('lang'),
                   first_seen_at=item['seen_at'],
                   last_seen_at=item['seen_at'],
                   source=item['source'],
                   source_urls=item['source_urls'])

    def merge_item(self, item):
        # overwrite with newer data
        if item['seen_at'] >= self.last_seen_at:
            self.title = item.get('title', self.title)
            self.company_name = item.get('company_name', self.company_name)
            self.locations = item.get('locations', self.locations)
            self.description_html = item.get('description_html', self.description_html)
            self.lang = item.get('lang', self.lang)
            self.source = item.get('source', self.source)

        # merge
        self.urls = list(set(self.urls + item['urls']))
        self.source_urls = list(set(self.source_urls + item.get('source_urls', [])))
        self.first_seen_at = min(self.first_seen_at, item['seen_at'])
        self.last_seen_at = max(self.last_seen_at, item['seen_at'])

        # bookkeeping
        self.items_merged_count += 1

    def to_api(self):
        return dict(title=self.title,
                    company_name=self.company_name,
                    urls=self.urls,
                    locations=self.locations,
                    first_seen_at=self.first_seen_at,
                    last_seen_at=self.last_seen_at,
                    lang=self.lang,
                    source=self.source)
