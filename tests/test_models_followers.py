from datetime import date

import pytest

from juniorguru.models.followers import Followers

from testing_utils import prepare_test_db


@pytest.fixture
def test_db():
    yield from prepare_test_db([Followers])


def test_names(test_db):
    Followers.add(month='2023-07', name='twitter', count=100)
    Followers.add(month='2023-07', name='facebook', count=200)
    Followers.add(month='2023-08', name='facebook', count=300)
    Followers.add(month='2023-10', name='youtube', count=50)

    assert list(Followers.names()) == ['facebook', 'twitter', 'youtube']


def test_months_range(test_db):
    Followers.add(month='2023-07', name='twitter', count=100)
    Followers.add(month='2023-07', name='facebook', count=200)
    Followers.add(month='2023-08', name='facebook', count=300)
    Followers.add(month='2023-10', name='youtube', count=50)

    assert Followers.months_range() == (date(2023, 7, 1), date(2023, 10, 1))


def test_breakdown(test_db):
    Followers.add(month='2023-07', name='twitter', count=100)
    Followers.add(month='2023-07', name='facebook', count=200)

    assert Followers.breakdown(date(2023, 7, 2)) == {'twitter': 100, 'facebook': 200}


def test_breakdown_months(test_db):
    Followers.add(month='2023-07', name='twitter', count=100)
    Followers.add(month='2023-07', name='facebook', count=200)
    Followers.add(month='2023-08', name='facebook', count=300)

    assert Followers.breakdown(date(2023, 8, 2)) == {'twitter': None, 'facebook': 300}


def test_breakdown_max(test_db):
    Followers.add(month='2023-07', name='twitter', count=100)
    Followers.add(month='2023-07', name='twitter', count=200)
    Followers.add(month='2023-07', name='twitter', count=300)

    assert Followers.breakdown(date(2023, 7, 2)) == {'twitter': 300}
