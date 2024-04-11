from typing import Iterable, Self

from peewee import CharField, IntegerField, TextField

from jg.coop.models.base import BaseModel


class DocumentedRole(BaseModel):
    club_id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    mention = CharField(unique=True)
    slug = CharField(unique=True)
    description = TextField()
    position = IntegerField(unique=True)
    emoji = CharField(null=True)
    color = IntegerField(null=True)
    icon_path = CharField(null=True)

    @classmethod
    def get_by_slug(cls, slug) -> Self:
        if not slug:
            raise ValueError(repr(slug))
        return cls.select().where(cls.slug == slug).get()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.position)
