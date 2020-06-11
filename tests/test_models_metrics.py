import pytest
from peewee import SqliteDatabase

from juniorguru.models import GlobalMetric, Job, JobMetric


@pytest.fixture
def db_connection():
    models = [GlobalMetric]
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
