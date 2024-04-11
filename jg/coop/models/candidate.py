from typing import Iterable, Self

from peewee import CharField

from jg.coop.models.base import BaseModel


class Candidate(BaseModel):
    name = CharField()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select()
