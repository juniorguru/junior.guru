from peewee import BooleanField, CharField, fn

from jg.coop.models.base import BaseModel


class GitHubSponsor(BaseModel):
    slug = CharField(primary_key=True)
    name = CharField(null=True)
    url = CharField()
    avatar_path = CharField()
    is_active = BooleanField()

    @classmethod
    def listing(cls):
        return (
            cls.select()
            .where(cls.is_active == True)  # noqa: E712
            .order_by(fn.random())
        )
