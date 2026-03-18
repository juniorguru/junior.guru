from peewee import CharField, IntegerField

from jg.coop.models.base import BaseModel


class Topic(BaseModel):
    name = CharField(primary_key=True)
    mentions_count = IntegerField(default=0)
    mentions_last_month_count = IntegerField(default=0)


class TopicChannel(BaseModel):
    name = CharField(primary_key=True)
    icon = CharField()
    content_size = IntegerField(default=0)
