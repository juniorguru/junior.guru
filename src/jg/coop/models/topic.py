from peewee import CharField, ForeignKeyField, IntegerField

from jg.coop.models.base import BaseModel
from jg.coop.models.club import ClubChannel


class TopicMention(BaseModel):
    name = CharField(primary_key=True)
    mentions_count = IntegerField(default=0)
    mentions_last_month_count = IntegerField(default=0)


class TopicDiscussion(BaseModel):
    name = CharField(primary_key=True)
    channels = ForeignKeyField(ClubChannel)
    icon = CharField()
    monthly_letters_count = IntegerField(default=0)

    @property
    def is_hot(self) -> bool:
        return self.monthly_letters_count > 50000

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.monthly_letters_count.desc())
