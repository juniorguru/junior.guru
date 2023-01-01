import re

from peewee import CharField

from juniorguru.models.base import BaseModel


NAME_SPLIT_RE = re.compile(r'[\s\-]+')

FEMININE_SURNAME_RE = re.compile(r'\w{2,}(o[vw][aá]$)|(ská$)')


class FeminineName(BaseModel):
    name = CharField(unique=True)

    @classmethod
    def is_feminine(cls, full_name):
        name_parts = NAME_SPLIT_RE.split(full_name.lower())
        for name in name_parts:
            if FEMININE_SURNAME_RE.search(name):
                return True
        for name in name_parts:
            if cls.get_or_none(cls.name == name):
                return True
        return False
