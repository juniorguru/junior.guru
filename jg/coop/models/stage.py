from typing import Iterable, Self

from peewee import CharField, IntegerField

from jg.coop.models.base import BaseModel
from jg.coop.models.page import Page


class Stage(BaseModel):
    position = IntegerField(unique=True)
    slug = CharField(unique=True)
    title = CharField()
    icon = CharField(unique=True)
    description = CharField()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.position)

    @property
    def list_pages(self) -> Iterable[Page]:
        return Page.stage_listing(self.slug)

    @property
    def list_todo_pages(self) -> Iterable[Page]:
        return Page.stage_todo_listing(self.slug)
