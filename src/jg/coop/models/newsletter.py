from peewee import CharField, ForeignKeyField

from jg.coop.models.base import BaseModel
from jg.coop.models.club import ClubMessage


class NewsletterTopic(BaseModel):
    name = CharField()
    text = CharField()
    emoji = CharField(unique=True)
    message = ForeignKeyField(ClubMessage, unique=True)
