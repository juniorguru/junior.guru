from peewee import BooleanField, CharField, DateField, TextField, IntegerField

from juniorguru.models.base import BaseModel, JSONField


# Experimenting with Czechitas. Calling the model 'employment' is stupid,
# but I needed to find a different name than 'job' so that the old model
# and the new model can co-exist for a while.


class Employment(BaseModel):
    class Meta:
        table_name = 'employment'  # TODO versions

    title = CharField()
    company_name = CharField()
    url = CharField(unique=True)
    apply_url = CharField(null=True)
    external_ids = JSONField(default=lambda: [])
    locations = JSONField(null=True)
    lang = CharField(null=True)
    description_html = TextField()
    first_seen_at = DateField()
    last_seen_at = DateField()

    # juniority
    juniority_re_score = IntegerField(null=True)
    juniority_ai_opinion = BooleanField(null=True)
    juniority_votes_score = IntegerField(null=True)
    juniority_votes_count = IntegerField(null=True)

    # meta information
    source = CharField()
    source_urls = JSONField(default=lambda: [])
    items_merged_count = IntegerField(default=0)

    @classmethod
    def get_by_item(cls, item):
        return cls.select() \
            .where(cls.url == item['url']) \
            .get()

    @classmethod
    def api_listing(cls):
        return cls.select() \
            .where((cls.juniority_re_score > 0) | cls.source == 'juniorguru') \
            .order_by(cls.last_seen_at.desc())

    @classmethod
    def from_item(cls, item):
        return cls(title=item['title'],
                   company_name=item['company_name'],
                   url=item['url'],
                   apply_url=item.get('apply_url'),
                   external_ids=item['external_ids'],
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
            self.apply_url = item.get('apply_url', self.apply_url)
            self.locations = item.get('locations', self.locations)
            self.description_html = item.get('description_html', self.description_html)
            self.lang = item.get('lang', self.lang)
            self.juniority_re_score = item.get('juniority_re_score', self.juniority_re_score)
            self.juniority_ai_opinion = item.get('juniority_ai_opinion', self.juniority_ai_opinion)
            self.juniority_votes_score = item.get('juniority_votes_score', self.juniority_votes_score)
            self.juniority_votes_count = item.get('juniority_votes_count', self.juniority_votes_count)
            self.source = item.get('source', self.source)

        # merge
        self.external_ids = list(set(self.external_ids + item.get('external_ids', [])))
        self.source_urls = list(set(self.source_urls + item.get('source_urls', [])))
        self.first_seen_at = min(self.first_seen_at, item['seen_at'])
        self.last_seen_at = max(self.last_seen_at, item['seen_at'])

        # bookkeeping
        self.items_merged_count += 1

    def to_api(self):
        return dict(title=self.title,
                    company_name=self.company_name,
                    url=self.url,
                    external_ids=self.external_ids,
                    locations=self.locations,
                    first_seen_at=self.first_seen_at,
                    last_seen_at=self.last_seen_at,
                    lang=self.lang,
                    source=self.source)
