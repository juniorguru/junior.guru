from datetime import date

import pytest
from peewee import SqliteDatabase

from juniorguru.models.followers import Followers


@pytest.fixture
def db_connection():
    db = SqliteDatabase(':memory:')
    with db:
        Followers.bind(db)
        Followers.create_table()
        yield db
        Followers.drop_table()


def test_names(db_connection):
    Followers.create(month='2023-07', name='twitter', count=100)
    Followers.create(month='2023-07', name='facebook', count=200)
    Followers.create(month='2023-08', name='facebook', count=300)
    Followers.create(month='2023-10', name='youtube', count=50)

    assert list(Followers.names()) == ['facebook', 'twitter', 'youtube']


def test_months_range(db_connection):
    Followers.create(month='2023-07', name='twitter', count=100)
    Followers.create(month='2023-07', name='facebook', count=200)
    Followers.create(month='2023-08', name='facebook', count=300)
    Followers.create(month='2023-10', name='youtube', count=50)

    assert Followers.months_range() == (date(2023, 7, 1), date(2023, 10, 1))


def test_breakdown(db_connection):
    Followers.create(month='2023-07', name='twitter', count=100)
    Followers.create(month='2023-07', name='facebook', count=200)

    assert Followers.breakdown(date(2023, 7, 2)) == {'twitter': 100, 'facebook': 200}


def test_breakdown_months(db_connection):
    Followers.create(month='2023-07', name='twitter', count=100)
    Followers.create(month='2023-07', name='facebook', count=200)
    Followers.create(month='2023-08', name='facebook', count=300)

    assert Followers.breakdown(date(2023, 8, 2)) == {'twitter': 0, 'facebook': 300}


def test_breakdown_max(db_connection):
    Followers.create(month='2023-07', name='twitter', count=100)
    Followers.create(month='2023-07', name='twitter', count=200)
    Followers.create(month='2023-07', name='twitter', count=300)

    assert Followers.breakdown(date(2023, 7, 2)) == {'twitter': 300}
