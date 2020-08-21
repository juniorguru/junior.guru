from peewee import CharField, DateTimeField

from juniorguru.models.base import BaseModel


class LastModified(BaseModel):
    path = CharField(primary_key=True)
    value = DateTimeField()

    @classmethod
    def get_value_by_path(cls, path):
        return cls.get(cls.path ** f'%{path}%').value
