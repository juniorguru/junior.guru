from peewee import CharField, IntegerField

from juniorguru.models.base import BaseModel


class Topic(BaseModel):
    name = CharField(primary_key=True)
    mentions_count = IntegerField(default=0)
    topic_channels_messages_count = IntegerField(default=0)
