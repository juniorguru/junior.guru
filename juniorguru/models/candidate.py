from typing import Iterable, Self

from peewee import CharField

from juniorguru.models.base import BaseModel


class Candidate(BaseModel):
    name = CharField()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select()
