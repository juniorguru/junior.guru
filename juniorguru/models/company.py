from datetime import date

from peewee import CharField, DateField, BooleanField

from juniorguru.models.base import BaseModel


class Company(BaseModel):
    name = CharField()
    filename = CharField()
    is_sponsoring_handbook = BooleanField(default=False)
    link = CharField()
    coupon = CharField(null=True)
    starts_at = DateField(null=True)
    expires_at = DateField(null=True)

    @classmethod
    def listing(cls, today=None):
        today = today or date.today()
        return cls.select() \
            .where(cls.starts_at <= today,
                   (cls.expires_at >= today) | cls.expires_at.is_null()) \
            .order_by(cls.starts_at, cls.name)

    @classmethod
    def handbook_listing(cls, today=None):
        today = today or date.today()
        return cls.listing() \
            .where(cls.is_sponsoring_handbook == True)
