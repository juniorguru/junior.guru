import pytest

from juniorguru.sync.members import get_coupon, get_active_subscription


def test_get_coupon():
    subscription = {'coupon': {'code': 'COUPON12345678'},
                    'createdAt': 1636922909,
                    'expiresAt': 1669668509,
                    'orders': [{'coupon': {'code': 'COUPON12345678'}, 'createdAt': 1638132692},
                               {'coupon': None, 'createdAt': 1636922909}]}

    assert get_coupon(subscription) == 'COUPON12345678'


def test_get_coupon_reads_coupon_property_with_priority():
    subscription = {'coupon': {'code': 'COUPON12345678'},
                    'createdAt': 1636922909,
                    'expiresAt': 1669668509,
                    'orders': []}

    assert get_coupon(subscription) == 'COUPON12345678'


def test_get_coupon_looks_at_last_order_if_no_coupon_property_set():
    subscription = {'coupon': None,
                    'createdAt': 1636922909,
                    'expiresAt': 1669668509,
                    'orders': [{'coupon': {'code': 'COUPON12345678'}, 'createdAt': 1637228062},
                               {'coupon': None, 'createdAt': 1636018061}]}

    assert get_coupon(subscription) == 'COUPON12345678'


def test_get_coupon_sorts_orders_by_date():
    subscription = {'coupon': None,
                    'createdAt': 1636922909,
                    'expiresAt': 1669668509,
                    'orders': [{'coupon': None, 'createdAt': 1636018061},
                               {'coupon': {'code': 'COUPON12345678'}, 'createdAt': 1637228062}]}

    assert get_coupon(subscription) == 'COUPON12345678'


def test_get_coupon_looks_at_last_order_only():
    subscription = {'coupon': None,
                    'createdAt': 1636922909,
                    'expiresAt': 1669668509,
                    'orders': [{'coupon': None, 'createdAt': 1637228062},
                               {'coupon': {'code': 'COUPON12345678'}, 'createdAt': 1636018061}]}

    assert get_coupon(subscription) is None


def test_get_active_subscription():
    assert get_active_subscription([
        dict(id=1, active=False),
        dict(id=2, active=True),
        dict(id=3, active=False),
    ]) == dict(id=2, active=True)


def test_get_active_subscription_multiple_active():
    with pytest.raises(ValueError):
        get_active_subscription([
            dict(id=1, active=True),
            dict(id=2, active=True),
            dict(id=3, active=False),
        ])


def test_get_active_subscription_no_active():
    with pytest.raises(ValueError):
        get_active_subscription([
            dict(id=1, active=False),
            dict(id=2, active=False),
            dict(id=3, active=False),
        ])


def test_get_active_subscription_no_items():
    with pytest.raises(ValueError):
        get_active_subscription([])
