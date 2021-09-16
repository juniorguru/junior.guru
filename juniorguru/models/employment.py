from peewee import CharField, DateField, TextField

from juniorguru.models.base import BaseModel


# Experimenting with Czechitas. Calling the model 'employment' is stupid,
# but I needed to find a different name than 'job' so that the old model
# and the new model can co-exist for a while.


class Employment(BaseModel):
    id = CharField(primary_key=True)
    title = CharField()
    company_name = CharField()
    url = CharField()
    description_html = TextField()
    first_seen_at = DateField()
    last_seen_at = DateField()
    source = CharField()
    source_url = CharField()

    @classmethod
    def api_listing(cls):
        return cls.select().order_by(cls.last_seen_at.desc())

    @classmethod
    def from_item(cls, item):
        return cls(id=item['id'],
                   title=item['title'],
                   company_name=item['company_name'],
                   url=item['url'],
                   description_html=item['description_html'],
                   first_seen_at=item['seen_at'],
                   last_seen_at=item['seen_at'],
                   source=item['source'],
                   source_url=item['source_url'])

    def merge_item(self, item):
        self.first_seen_at = min(self.first_seen_at, item['seen_at'])
        self.last_seen_at = max(self.last_seen_at, item['seen_at'])

    def to_api(self):
        return dict(title=self.title,
                    company_name=self.company_name,
                    url=self.url,
                    description_html=self.description_html,
                    first_seen_at=self.first_seen_at,
                    last_seen_at=self.last_seen_at,
                    source=self.source)
