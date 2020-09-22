import pytest
from peewee import SqliteDatabase

from juniorguru.models import SpiderMetric


@pytest.fixture
def db_connection():
    models = [SpiderMetric]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


def test_spider_metric_as_dict(db_connection):
    SpiderMetric.create(spider_name='li', name='item_saved_count', value=1200)
    SpiderMetric.create(spider_name='li', name='item_dropped_count', value=6400)
    SpiderMetric.create(spider_name='jg', name='item_saved_count', value=800)
    SpiderMetric.create(spider_name='jg', name='item_dropped_count', value=100)
    SpiderMetric.create(spider_name='jg', name='elapsed_time_seconds', value=3000)
    SpiderMetric.create(spider_name='sj', name='elapsed_time_seconds', value=4)

    assert SpiderMetric.as_dict() == {
        'item_saved_count': {'jg': 800, 'li': 1200, 'sj': 0},
        'item_dropped_count': {'jg': 100, 'li': 6400, 'sj': 0},
        'elapsed_time_seconds': {'jg': 3000, 'li': 0, 'sj': 4},
    }
