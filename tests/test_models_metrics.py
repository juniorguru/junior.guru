from datetime import datetime, timedelta

import pytest
from peewee import SqliteDatabase

from juniorguru.models import GlobalMetric, Job, JobMetric
from testing_utils import create_job


@pytest.fixture
def db_connection():
    models = [GlobalMetric, Job, JobMetric]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


def test_global_metric_as_dict(db_connection):
    metric1 = GlobalMetric.create(name='avg_monthly_users', value=1200)
    metric2 = GlobalMetric.create(name='avg_monthly_pageviews', value=6400)

    assert GlobalMetric.as_dict() == {
        'avg_monthly_users': 1200,
        'avg_monthly_pageviews': 6400,
    }


def test_calc_avg_daily_per_job(db_connection):
    job1 = create_job('1', posted_at=datetime.utcnow() - timedelta(days=15))
    job2 = create_job('2', posted_at=datetime.utcnow() - timedelta(days=5))
    JobMetric.create(job=job1, name='users', value=2)
    JobMetric.create(job=job1, name='pageviews', value=1)
    JobMetric.create(job=job2, name='users', value=5)
    JobMetric.create(job=job2, name='pageviews', value=5)

    assert JobMetric.calc_avg_daily_per_job('users') == (2 / 14 + 5 / 4) / 2
