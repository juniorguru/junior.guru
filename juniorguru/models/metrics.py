from peewee import CharField, ForeignKeyField, IntegerField

from juniorguru.models import Job
from juniorguru.models.base import BaseModel


JOB_METRIC_NAMES = [
    'users',
    'pageviews',
    'applications',
]


class GlobalMetric(BaseModel):
    name = CharField(choices=[
        ('avg_monthly_users', None),
        ('avg_monthly_pageviews', None),
        ('subscribers', None),
    ])
    value = IntegerField()

    @classmethod
    def as_dict(cls):
        return {metric.name: metric.value for metric in cls.select()}


class JobMetric(BaseModel):
    job = ForeignKeyField(Job, backref='_metrics')
    name = CharField(choices=[(n, None) for n in JOB_METRIC_NAMES])
    value = IntegerField()
