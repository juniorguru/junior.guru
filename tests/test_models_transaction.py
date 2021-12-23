from datetime import date, timedelta

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Transaction
from juniorguru.models.transaction import get_year_ago


@pytest.fixture
def db_connection():
    db = SqliteDatabase(':memory:')
    with db:
        Transaction.bind(db)
        Transaction.create_table()
        yield db
        Transaction.drop_table()


def create_transaction(**kwargs):
    return Transaction.create(
        happened_on=kwargs.get('happened_on', date.today() - timedelta(days=3)),
        category=kwargs.get('category', 'abcd'),
        amount=kwargs.get('amount', 1038)
    )


@pytest.mark.parametrize('today, expected', [
    pytest.param(date(2021, 8, 30), date(2020, 8, 30), id='random specific date'),
    pytest.param(date(2020, 2, 29), date(2019, 2, 28), id='leap year'),
])
def test_get_year_ago(today, expected):
    assert get_year_ago(today) == expected


def test_listing(db_connection):
    t1 = create_transaction()
    t2 = create_transaction()

    assert set(Transaction.listing()) == {t1, t2}


@pytest.mark.parametrize('happened_on, today', [
    pytest.param(date.today(), None, id='today implicitly'),
    pytest.param(date.today(), date.today(), id='today explicitly'),
    pytest.param(date(2021, 8, 30), date(2021, 8, 30), id='random specific date'),
    pytest.param(date(2020, 2, 29), date(2020, 2, 29), id='leap year'),
])
def test_listing_uses_only_past_12_months_from_given_date(db_connection, happened_on, today):
    t1 = create_transaction(happened_on=happened_on)
    t2 = create_transaction(happened_on=happened_on - timedelta(days=150))
    t3 = create_transaction(happened_on=happened_on - timedelta(days=250))
    t4 = create_transaction(happened_on=happened_on - timedelta(days=350))
    create_transaction(happened_on=happened_on + timedelta(days=1))
    create_transaction(happened_on=happened_on - timedelta(days=450))

    assert set(Transaction.listing(today)) == {t1, t2, t3, t4}


def test_listing_sorts_from_newest_to_oldest(db_connection):
    t1 = create_transaction(happened_on=date.today() - timedelta(days=250))
    t2 = create_transaction()
    t3 = create_transaction(happened_on=date.today() - timedelta(days=150))
    t4 = create_transaction(happened_on=date.today() - timedelta(days=350))

    assert list(Transaction.listing()) == [t2, t3, t1, t4]


def test_incomes_breakdown(db_connection):
    create_transaction(amount=200, category='a')
    create_transaction(amount=100, category='a')
    create_transaction(amount=500, category='b')
    create_transaction(amount=100, category='c')

    assert Transaction.incomes_breakdown() == {
        'a': 300,
        'b': 500,
        'c': 100,
    }


def test_incomes_breakdown_ignores_expenses(db_connection):
    create_transaction(amount=100, category='a')
    create_transaction(amount=-100, category='b')

    assert Transaction.incomes_breakdown() == {
        'a': 100,
    }


def test_incomes_breakdown_ignores_tax_returns(db_connection):
    create_transaction(amount=100, category='tax')
    create_transaction(amount=100, category='a')

    assert Transaction.incomes_breakdown() == {
        'a': 100,
    }


def test_expenses_breakdown(db_connection):
    create_transaction(amount=-200, category='a')
    create_transaction(amount=-100, category='a')
    create_transaction(amount=-500, category='b')
    create_transaction(amount=-100, category='c')

    assert Transaction.expenses_breakdown() == {
        'a': 300,
        'b': 500,
        'c': 100,
    }


def test_expenses_breakdown_ignores_incomes(db_connection):
    create_transaction(amount=-100, category='a')
    create_transaction(amount=100, category='b')

    assert Transaction.expenses_breakdown() == {
        'a': 100,
    }


def test_expenses_breakdown_ignores_salary(db_connection):
    create_transaction(amount=-100, category='salary')
    create_transaction(amount=-100, category='a')

    assert Transaction.expenses_breakdown() == {
        'a': 100,
    }


def test_expenses_breakdown_inlcudes_tax_returns(db_connection):
    create_transaction(amount=100, category='tax')
    create_transaction(amount=-1000, category='tax')

    assert Transaction.expenses_breakdown() == {
        'tax': 900,
    }


def test_profit_monthly(db_connection):
    create_transaction(amount=-1000, category='salary', happened_on=date(2020, 2, 2))
    create_transaction(amount=55, category='a', happened_on=date(2020, 3, 1))
    create_transaction(amount=100, category='b', happened_on=date(2020, 4, 3))
    create_transaction(amount=500, category='c', happened_on=date(2020, 6, 6))
    create_transaction(amount=-300, category='d', happened_on=date(2020, 11, 9))

    assert Transaction.profit_monthly(date(2020, 12, 12)) == 30
