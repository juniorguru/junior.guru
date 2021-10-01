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
                   remote=item['remote'],
                   description_html=item['description_html'],
                   description_text=item['description_text'],
                   lang=item.get('lang'),
                   first_seen_at=item['seen_at'],
                   last_seen_at=item['seen_at'],
                   employment_types=item['employment_types'],
                   source=item['source'],
                   source_urls=item['source_urls'])

    def merge_item(self, item):
        # overwrite with newer data
        if item['seen_at'] >= self.last_seen_at:
            overwrite_attrs = [
                'title', 'company_name', 'apply_url', 'locations', 'remote', 'description_html', 'description_text',
                'lang', 'juniority_re_score', 'juniority_ai_opinion', 'juniority_votes_score', 'juniority_votes_count',
                'employment_types', 'source',
            ]
            for attr in overwrite_attrs:
                old_value = getattr(self, attr)
                new_value = item.get(attr, old_value)
                setattr(self, attr, new_value)

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
                    remote=self.remote,
                    first_seen_at=self.first_seen_at,
                    last_seen_at=self.last_seen_at,
                    lang=self.lang,
                    juniority_score=self.juniority_re_score,
                    employment_types=self.employment_types,
                    source=self.source)
