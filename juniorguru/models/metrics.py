from datetime import date, timedelta
from itertools import groupby
from operator import attrgetter

from peewee import CharField, FloatField, ForeignKeyField

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
        ('avg_daily_users_per_job', None),
        ('avg_daily_pageviews_per_job', None),
        ('avg_daily_applications_per_job', None),
    ])
    value = FloatField()

    @classmethod
    def as_dict(cls):
        return {metric.name: metric.value for metric in cls.select()}


class JobMetric(BaseModel):
    job = ForeignKeyField(Job, backref='list_metrics')
    name = CharField(choices=[(n, None) for n in JOB_METRIC_NAMES])
    value = FloatField()

    @classmethod
    def calc_avg_daily_per_job(cls, name, today=None):
        if name not in JOB_METRIC_NAMES:
            raise ValueError(name)

        # the per job data is up to yesterday
        yesterday = date.today() - timedelta(days=1)

        # calculating stats only for jobs added to JG directly as we don't
        # have information about how many days the scraped jobs have been
        # displayed (also: this is the number which should grow, JG is
        # the main thing)
        relevant_jobs = list(Job.juniorguru())
        metrics = cls.select() \
            .where(cls.name == name, cls.job.in_(relevant_jobs)) \
            .order_by(cls.job)  # ordering here for the groupby below

        values_per_day = []
        for job, metrics_per_job in groupby(metrics, key=attrgetter('job')):
            days = (yesterday - job.posted_at.date()).days
            values_per_day.extend((metric.value / days) for metric in metrics_per_job)
        return sum(values_per_day) / len(relevant_jobs)
