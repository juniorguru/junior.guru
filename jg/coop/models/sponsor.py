from peewee import BooleanField, CharField, DateField

from jg.coop.models.base import BaseModel


class GitHubSponsor(BaseModel):
    slug = CharField(primary_key=True)
    name = CharField(null=True)
    url = CharField()
    avatar_url = CharField()
    sponsored_on = DateField()
    is_active = BooleanField()
