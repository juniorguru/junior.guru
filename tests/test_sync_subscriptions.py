from datetime import date

import pytest

from juniorguru.sync.subscriptions import (format_date, get_active_coupon,
                                           get_student_months, get_student_started_on)


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
