from typing import Iterable, Literal, Self

from peewee import CharField, DateField, IntegerField, TextField, fn

from jg.coop.models.base import BaseModel, JSONField
from jg.coop.models.club import ClubUser


class Partner(BaseModel):
    # organization
    slug = CharField(primary_key=True)
    name = CharField()
    url = CharField()
    cz_business_id = IntegerField(null=True)
    sk_business_id = IntegerField(null=True)
    subscription_id = IntegerField(null=True)
    logo_path = CharField()
    role_id = IntegerField(null=True)
    members_ids = JSONField(default=list)

    # partner
    plan_id = IntegerField()
    start_on = DateField()
    note = TextField()
    role_id = IntegerField(null=True)

    @property
    def utm_campaign(self) -> Literal["partnership"]:
        return "partnership"

    @property
    def list_members(self) -> Iterable[ClubUser]:
        return ClubUser.select().where(ClubUser.account_id.in_(self.members_ids))

    @property
    def members_count(self) -> int:
        return len(self.members_ids)

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(fn.czech_sort(cls.name))

    @classmethod
    def count(cls) -> int:
        return cls.select().count()
