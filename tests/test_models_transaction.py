from datetime import date, timedelta

import pytest
from peewee import SqliteDatabase

from juniorguru.models.transaction import Transaction


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


def test_listing_sorts_from_newest_to_oldest(db_connection):
    t1 = create_transaction(happened_on=date(2021, 8, 31))
    t2 = create_transaction(happened_on=date(2021, 8, 1))
    t3 = create_transaction(happened_on=date(2021, 8, 15))

    assert list(Transaction.listing(date(2021, 1, 1), date(2021, 12, 31))) == [t1, t3, t2]


# def test_ttm_listing_uses_today_implicitly(db_connection):
#     t1 = create_transaction(happened_on=date.today())
#     create_transaction(happened_on=date.today() + timedelta(days=1))
#     create_transaction(happened_on=date.today() - timedelta(days=450))

#     assert set(Transaction.ttm_listing()) == {t1}


# @pytest.mark.parametrize('today', [
#     pytest.param(date(2021, 8, 30), id='random specific date'),
#     pytest.param(date(2020, 2, 29), id='leap year'),
# ])
# def test_ttm_listing_uses_only_past_12_months_from_given_date(db_connection, today):
#     t1 = create_transaction(happened_on=today)
#     t2 = create_transaction(happened_on=today - timedelta(days=150))
#     t3 = create_transaction(happened_on=today - timedelta(days=250))
#     t4 = create_transaction(happened_on=today - timedelta(days=350))
#     create_transaction(happened_on=today + timedelta(days=1))
#     create_transaction(happened_on=today - timedelta(days=450))

#     assert set(Transaction.ttm_listing(today)) == {t1, t2, t3, t4}


# def test_ttm_listing_sorts_from_newest_to_oldest(db_connection):
#     t1 = create_transaction(happened_on=date.today() - timedelta(days=250))
#     t2 = create_transaction()
#     t3 = create_transaction(happened_on=date.today() - timedelta(days=150))
#     t4 = create_transaction(happened_on=date.today() - timedelta(days=350))

#     assert list(Transaction.ttm_listing()) == [t2, t3, t1, t4]


# def test_month_listing_uses_today_implicitly(db_connection):
#     t1 = create_transaction(happened_on=date.today().replace(day=1))
#     t2 = create_transaction(happened_on=date.today())
#     create_transaction(happened_on=date.today() - timedelta(days=40))
#     create_transaction(happened_on=date.today() + timedelta(days=40))

#     assert set(Transaction.month_listing()) == {t1, t2}


# def test_month_listing_uses_only_past_and_future_days_of_given_days_month(db_connection):
#     t1 = create_transaction(happened_on=date(2021, 8, 1))
#     t2 = create_transaction(happened_on=date(2021, 8, 15))
#     t3 = create_transaction(happened_on=date(2021, 8, 31))
#     create_transaction(happened_on=date(2021, 7, 31))
#     create_transaction(happened_on=date(2021, 9, 1))

#     assert set(Transaction.month_listing()) == {t1, t2, t3}


# def test_incomes_breakdown(db_connection):
#     create_transaction(amount=200, category='a')
#     create_transaction(amount=100, category='a')
#     create_transaction(amount=500, category='b')
#     create_transaction(amount=100, category='c')

#     assert Transaction.incomes_breakdown() == {
#         'a': 300,
#         'b': 500,
#         'c': 100,
#     }


# def test_incomes_breakdown_ignores_expenses(db_connection):
#     create_transaction(amount=100, category='a')
#     create_transaction(amount=-100, category='b')

#     assert Transaction.incomes_breakdown() == {
#         'a': 100,
#     }


# def test_incomes_breakdown_ignores_tax_returns(db_connection):
#     create_transaction(amount=100, category='tax')
#     create_transaction(amount=100, category='a')

#     assert Transaction.incomes_breakdown() == {
#         'a': 100,
#     }


# def test_expenses_breakdown(db_connection):
#     create_transaction(amount=-200, category='a')
#     create_transaction(amount=-100, category='a')
#     create_transaction(amount=-500, category='b')
#     create_transaction(amount=-100, category='c')

#     assert Transaction.expenses_breakdown() == {
#         'a': 300,
#         'b': 500,
#         'c': 100,
#     }


# def test_expenses_breakdown_ignores_incomes(db_connection):
#     create_transaction(amount=-100, category='a')
#     create_transaction(amount=100, category='b')

#     assert Transaction.expenses_breakdown() == {
#         'a': 100,
#     }


# def test_expenses_breakdown_ignores_salary(db_connection):
#     create_transaction(amount=-100, category='salary')
#     create_transaction(amount=-100, category='a')

#     assert Transaction.expenses_breakdown() == {
#         'a': 100,
#     }


# def test_expenses_breakdown_inlcudes_tax_returns(db_connection):
#     create_transaction(amount=100, category='tax')
#     create_transaction(amount=-1000, category='tax')

#     assert Transaction.expenses_breakdown() == {
#         'tax': 900,
#     }


# def test_profit_monthly(db_connection):
#     create_transaction(amount=-1000, category='salary', happened_on=date(2020, 2, 2))
#     create_transaction(amount=55, category='a', happened_on=date(2020, 3, 1))
#     create_transaction(amount=100, category='b', happened_on=date(2020, 4, 3))
#     create_transaction(amount=500, category='c', happened_on=date(2020, 6, 6))
#     create_transaction(amount=-300, category='d', happened_on=date(2020, 11, 9))

#     assert Transaction.profit_monthly(date(2020, 12, 12)) == 30
