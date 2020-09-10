from datetime import date

from peewee import CharField, DateField, IntegerField, ForeignKeyField

from juniorguru.models.base import BaseModel


class Logo(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    filename = CharField()
    email = CharField()
    link = CharField()
    months = IntegerField()
    starts_at = DateField()
    expires_at = DateField()

    @classmethod
    def listing(cls, today=None):
        today = today or date.today()
        return cls.select() \
            .where(cls.starts_at <= today, cls.expires_at >= today) \
            .order_by(cls.months.desc(), cls.starts_at)


class LogoMetric(BaseModel):
    logo = ForeignKeyField(Logo, backref='list_metrics')
    name = CharField(choices=['clicks_per_logo'], default='clicks_per_logo')
    value = IntegerField()
