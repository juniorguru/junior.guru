from peewee import CharField, IntegerField

from juniorguru.models.base import BaseModel


class Metric(BaseModel):
    name = CharField(primary_key=True)
    value = IntegerField()

    @classmethod
    def as_dict(cls):
        return {metric.name: metric.value for metric in cls.select()}
