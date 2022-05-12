from peewee import CharField, BooleanField, IntegerField

from juniorguru.models.base import BaseModel, JSONField


class Mentor(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    company = CharField(null=True)
    topics = JSONField(default=lambda: [])
    book_url = CharField(null=True)
    english_only = BooleanField(default=False)


    @classmethod
    def listing(cls):
        return cls.select()
