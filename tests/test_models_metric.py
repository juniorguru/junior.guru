import pytest
from peewee import SqliteDatabase

from juniorguru.models import Metric


@pytest.fixture
def db_connection():
    models = [Metric]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


def test_metric_as_dict(db_connection):
    Metric.create(name='avg_monthly_users', value=1200)
    Metric.create(name='avg_monthly_pageviews', value=6400)

    assert Metric.as_dict() == {
        'avg_monthly_users': 1200,
        'avg_monthly_pageviews': 6400,
    }
