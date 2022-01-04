from peewee import CharField, IntegerField

from juniorguru.models.base import BaseModel


class PodcastEpisode(BaseModel):
    id = CharField()
    number = IntegerField()
    title = CharField()
    media_url = CharField()
    media_size = IntegerField()
    media_type = CharField()
    media_duration_s = IntegerField()
    # date = DateField(index=True)
    # image_path = CharField()
    # tags = JSONField(default=lambda: [])
