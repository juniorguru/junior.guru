from typing import Iterable, Self

from peewee import CharField, IntegerField, TextField

from jg.coop.models.base import BaseModel


class Tip(BaseModel):
    slug = CharField(primary_key=True)
    position = IntegerField(unique=True)
    emoji = CharField(unique=True)
    title = CharField()
    title_text = CharField()
    edit_url = CharField()
    discord_url = CharField()
    lead = TextField()
    content = TextField()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.position)
