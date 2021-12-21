from datetime import date, timedelta

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Transaction


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
        category=kwargs.get('category', 'memberships'),
        amount=kwargs.get('amount', 1038)
    )


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


# def test_incomes_breakdown(db_connection):
#     create_transaction(amount=200, category='donations')
#     create_transaction(amount=100, category='donations')
#     create_transaction(amount=500, category='partnerships')
#     create_transaction(amount=100, category='jobs')

#     assert Transaction.incomes_breakdown(date.today()) == {
#         'donations': 300,
#         'partnerships': 500,
#         'jobs': 100,
#     }


# def test_incomes_breakdown_ignores_expenses(db_connection):
#     create_transaction(amount=100, category='jobs')
#     create_transaction(amount=-100, category='tax')

#     assert Transaction.incomes_breakdown(date.today()) == {
#         'jobs': 100,
#     }


# def test_incomes_breakdown_uses_only_past_12_months(db_connection):
#     create_transaction(amount=100, category='jobs')
#     create_transaction(amount=100, category='donations', happened_on=date.today() - timedelta(days=400))

#     assert Transaction.incomes_breakdown(date.today()) == {
#         'jobs': 100,
#     }


# def test_expenses_breakdown(db_connection):
#     create_transaction(amount=-200, category='discord')
#     create_transaction(amount=-100, category='discord')
#     create_transaction(amount=-500, category='lawyer')
#     create_transaction(amount=-100, category='tax')

#     assert Transaction.expenses_breakdown(date.today()) == {
#         'discord': 300,
#         'lawyer': 500,
#         'tax': 100,
#     }


# def test_expenses_breakdown_ignores_incomes(db_connection):
#     create_transaction(amount=-100, category='tax')
#     create_transaction(amount=100, category='donations')

#     assert Transaction.expenses_breakdown(date.today()) == {
#         'tax': 100,
#     }


# def test_expenses_breakdown_uses_only_past_12_months(db_connection):
#     create_transaction(amount=-100, category='tax')
#     create_transaction(amount=-100, category='discord', happened_on=date.today() - timedelta(days=400))

#     assert Transaction.expenses_breakdown(date.today()) == {
#         'tax': 100,
#     }
