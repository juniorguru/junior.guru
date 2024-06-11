from peewee import BooleanField, CharField, DateField, fn

from jg.coop.models.base import BaseModel


class GitHubSponsor(BaseModel):
    slug = CharField(primary_key=True)
    name = CharField(null=True)
    url = CharField()
    avatar_url = CharField()
    is_active = BooleanField()

    @classmethod
    def listing(cls):
        return cls.select().where(cls.is_active == True).order_by(fn.random())
