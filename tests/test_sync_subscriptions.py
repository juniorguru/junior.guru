from datetime import date

import pytest

from juniorguru.sync.subscriptions import (format_date, get_active_coupon,
                                           get_student_months, get_student_started_on, get_subscribed_periods,
                                           get_subscriptions)


def test_get_active_coupon():
    subscription = {'coupon': {'code': 'COUPON12345678'},
                    'createdAt': 1636922909,
                    'expiresAt': 1669668509,
                    'orders': [{'coupon': {'code': 'COUPON12345678'}, 'createdAt': 1638132692},
                               {'coupon': None, 'createdAt': 1636922909}]}

    assert get_active_coupon(subscription) == 'COUPON12345678'


def test_get_active_coupon_reads_coupon_property_with_priority():
    subscription = {'coupon': {'code': 'COUPON12345678'},
                    'createdAt': 1636922909,
                    'expiresAt': 1669668509,
                    'orders': []}

    assert get_active_coupon(subscription) == 'COUPON12345678'


def test_get_active_coupon_looks_at_last_order_if_no_coupon_property_set():
    subscription = {'coupon': None,
                    'createdAt': 1636922909,
                    'expiresAt': 1669668509,
                    'orders': [{'coupon': {'code': 'COUPON12345678'}, 'createdAt': 1637228062},
                               {'coupon': None, 'createdAt': 1636018061}]}

    assert get_active_coupon(subscription) == 'COUPON12345678'


def test_get_active_coupon_sorts_orders_by_date():
    subscription = {'coupon': None,
                    'createdAt': 1636922909,
                    'expiresAt': 1669668509,
                    'orders': [{'coupon': None, 'createdAt': 1636018061},
                               {'coupon': {'code': 'COUPON12345678'}, 'createdAt': 1637228062}]}

    assert get_active_coupon(subscription) == 'COUPON12345678'


def test_get_active_coupon_looks_at_last_order_only():
    subscription = {'coupon': None,
                    'createdAt': 1636922909,
                    'expiresAt': 1669668509,
                    'orders': [{'coupon': None, 'createdAt': 1637228062},
                               {'coupon': {'code': 'COUPON12345678'}, 'createdAt': 1636018061}]}

    assert get_active_coupon(subscription) is None


def test_get_student_months():
    subscription = {'orders': [{'coupon': {'code': 'STUDENTCOUPON12345678'}, 'createdAt': 1636018061}]}

    assert get_student_months(subscription, 'STUDENTCOUPON12345678') == ['2021-11']


def test_get_student_months_compares_coupon_as_prefix():
    subscription = {'orders': [{'coupon': {'code': 'STUDENTCOUPON12345678'}, 'createdAt': 1636018061}]}

    assert get_student_months(subscription, 'STUDENTCOUPON') == ['2021-11']


def test_get_student_months_no_orders():
    subscription = {'orders': []}

    assert get_student_months(subscription, 'STUDENTCOUPON12345678') == []


def test_get_student_months_ignores_other_coupons():
    subscription = {'orders': [{'coupon': {'code': 'COUPON12345678'}, 'createdAt': 1637228062},
                               {'coupon': {'code': 'STUDENTCOUPON12345678'}, 'createdAt': 1636018061}]}

    assert get_student_months(subscription, 'STUDENTCOUPON12345678') == ['2021-11']


def test_get_student_months_ignores_orders_without_coupons():
    subscription = {'orders': [{'coupon': None, 'createdAt': 1637228062},
                               {'coupon': {'code': 'STUDENTCOUPON12345678'}, 'createdAt': 1636018061}]}

    assert get_student_months(subscription, 'STUDENTCOUPON12345678') == ['2021-11']


def test_get_student_months_multiple_sorted_asc():
    subscription = {'orders': [{'coupon': {'code': 'STUDENTCOUPON12345678'},
                                'createdAt': 1648895520},
                               {'coupon': {'code': 'STUDENTCOUPON12345678'},
                                'createdAt': 1646217071},
                               {'coupon': {'code': 'STUDENTCOUPON12345678'},
                                'createdAt': 1643797924},
                               {'coupon': None,
                                'createdAt': 1642588223}]}

    assert get_student_months(subscription, 'STUDENTCOUPON12345678') == [
        '2022-02',
        '2022-03',
        '2022-04',
    ]


def test_get_student_started_on():
    subscription = {'orders': [{'coupon': {'code': 'STUDENTCOUPON12345678'}, 'createdAt': 1636018061}]}

    assert get_student_started_on(subscription, 'STUDENTCOUPON12345678') == date(2021, 11, 4)


def test_get_student_started_on_compares_coupon_as_prefix():
    subscription = {'orders': [{'coupon': {'code': 'STUDENTCOUPON12345678'}, 'createdAt': 1636018061}]}

    assert get_student_started_on(subscription, 'STUDENTCOUPON') == date(2021, 11, 4)


def test_get_student_started_on_no_orders():
    subscription = {'orders': []}

    assert get_student_started_on(subscription, 'STUDENTCOUPON12345678') is None


def test_get_student_started_on_ignores_other_coupons():
    subscription = {'orders': [{'coupon': {'code': 'COUPON12345678'}, 'createdAt': 1637228062},
                               {'coupon': {'code': 'STUDENTCOUPON12345678'}, 'createdAt': 1636018061}]}

    assert get_student_started_on(subscription, 'STUDENTCOUPON12345678') == date(2021, 11, 4)


def test_get_student_started_on_ignores_orders_without_coupons():
    subscription = {'orders': [{'coupon': None, 'createdAt': 1637228062},
                               {'coupon': {'code': 'STUDENTCOUPON12345678'}, 'createdAt': 1636018061}]}

    assert get_student_started_on(subscription, 'STUDENTCOUPON12345678') == date(2021, 11, 4)


def test_get_student_started_on_multiple_sorted_asc():
    subscription = {'orders': [{'coupon': {'code': 'STUDENTCOUPON12345678'},
                                'createdAt': 1648895520},
                               {'coupon': {'code': 'STUDENTCOUPON12345678'},
                                'createdAt': 1646217071},
                               {'coupon': {'code': 'STUDENTCOUPON12345678'},
                                'createdAt': 1643797924},
                               {'coupon': None,
                                'createdAt': 1642588223}]}

    assert get_student_started_on(subscription, 'STUDENTCOUPON12345678') == date(2022, 2, 2)


@pytest.mark.parametrize('value, expected', [
    (None, None),
    (date(2022, 2, 4), '2022-02-04'),
])
def test_format_date(value, expected):
    assert format_date(value) == expected


def test_get_subscriptions():
    graphql_results = [{
        'subscriptions': {
            'edges': [
                {'node': 1},
                {'node': 2},
                {'node': 3},
            ]
        }
    },
    {
        'subscriptions': {
            'edges': [
                {'node': 4},
                {'node': 5},
            ]
        }
    }]
    subscriptions = get_subscriptions(graphql_results)

    assert list(subscriptions) == [1, 2, 3, 4, 5]


def test_get_subscribed_periods():
    subscription = {'id': '123456789',
                    'active': True,
                    'createdAt': 1629300930,
                    'expiresAt': 1654097730,
                    'pastDue': False,
                    'coupon': None,
                    'member': {},
                    'orders': [
                        {'createdAt': 1651419692, 'coupon': None},
                        {'createdAt': 1648827722, 'coupon': None},
                        {'createdAt': 1646149282, 'coupon': None},
                        {'createdAt': 1643730158, 'coupon': None},
                        {'createdAt': 1641051710, 'coupon': None},
                        {'createdAt': 1638373347, 'coupon': None},
                        {'createdAt': 1635781082, 'coupon': {'code': 'COUPON12345678'}},
                        {'createdAt': 1633103366, 'coupon': {'code': 'STUDENTGARGAMEL69320144V2'}},
                        {'createdAt': 1630510548, 'coupon': {'code': 'COUPON12345678'}},
                        {'createdAt': 1629300930, 'coupon': None}
                    ]}

    assert list(get_subscribed_periods(subscription)) == [
        {'start_on': date(2022, 5, 1), 'end_on': date(2022, 5, 31), 'coupon_base': None},
        {'start_on': date(2022, 4, 1), 'end_on': date(2022, 4, 30), 'coupon_base': None},
        {'start_on': date(2022, 3, 1), 'end_on': date(2022, 3, 31), 'coupon_base': None},
        {'start_on': date(2022, 2, 1), 'end_on': date(2022, 2, 28), 'coupon_base': None},
        {'start_on': date(2022, 1, 1), 'end_on': date(2022, 1, 31), 'coupon_base': None},
        {'start_on': date(2021, 12, 1), 'end_on': date(2021, 12, 31), 'coupon_base': None},
        {'start_on': date(2021, 11, 1), 'end_on': date(2021, 11, 30), 'coupon_base': 'COUPON12345678'},
        {'start_on': date(2021, 10, 1), 'end_on': date(2021, 10, 31), 'coupon_base': 'STUDENTGARGAMEL69320144'},
        {'start_on': date(2021, 9, 1), 'end_on': date(2021, 9, 30), 'coupon_base': 'COUPON12345678'},
        {'start_on': date(2021, 8, 18), 'end_on': date(2021, 8, 31), 'coupon_base': None},
    ]


def test_get_subscribed_periods_different_created_at():
    subscription = {'id': '123456789',
                    'active': True,
                    'createdAt': 1619817670,
                    'expiresAt': 1652563270,
                    'pastDue': False,
                    'coupon': None,
                    'member': {},
                    'orders': [
                        {'coupon': None, 'createdAt': 1621027502},
                        {'coupon': None, 'createdAt': 1619817671}
                    ]}

    assert list(get_subscribed_periods(subscription)) == [
        {'start_on': date(2021, 5, 14), 'end_on': date(2022, 5, 13), 'coupon_base': None},
        {'start_on': date(2021, 4, 30), 'end_on': date(2021, 5, 13), 'coupon_base': None},
    ]


def test_get_subscribed_periods_no_orders():
    subscription = {'id': '123456789',
                    'active': True,
                    'createdAt': 1619817670,
                    'expiresAt': 1652563270,
                    'pastDue': False,
                    'coupon': None,
                    'member': {},
                    'orders': []}

    assert list(get_subscribed_periods(subscription)) == []
