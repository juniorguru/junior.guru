from peewee import CharField, DateField, IntegerField, ForeignKeyField

from juniorguru.models.base import BaseModel


class Logo(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    email = CharField()
    link = CharField()
    months = IntegerField()
    starts_at = DateField()
    expires_at = DateField()

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.months.desc(), cls.starts_at)


class LogoMetric(BaseModel):
    logo = ForeignKeyField(Logo, backref='list_metrics')
    name = CharField(choices=['clicks_per_logo'], default='clicks_per_logo')
    value = IntegerField()
