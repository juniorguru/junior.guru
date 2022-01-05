import arrow
from peewee import CharField, IntegerField, DateTimeField

from juniorguru.models.base import BaseModel


class PodcastEpisode(BaseModel):
    id = CharField()
    number = IntegerField()
    published_at = DateTimeField(index=True)
    title = CharField()
    media_url = CharField()
    media_size = IntegerField()
    media_type = CharField()
    media_duration_s = IntegerField()

    @property
    def title_numbered(self):
        return f"#{self.number} {self.title}"

    @property
    def published_at_prg(self):
        return arrow.get(self.published_at, 'Europe/Prague').datetime

    @classmethod
    def api_listing(cls):
        return cls.select().order_by(cls.published_at.desc())
