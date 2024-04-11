from datetime import date, datetime

import pytest

from jg.coop.sync.members import get_active_subscription, get_coupon, get_expires_at


PLAN_CLUB = dict(planGroup=dict(name="abc"))

PLAN_OTHER = dict(planGroup=None)


def test_get_coupon():
    subscription = {
        "coupon": {"code": "COUPON12345678"},
        "createdAt": 1636922909,
        "expiresAt": 1669668509,
        "orders": [
            {"coupon": {"code": "COUPON12345678"}, "createdAt": 1638132692},
            {"coupon": None, "createdAt": 1636922909},
        ],
    }

    assert get_coupon(subscription) == "COUPON12345678"


def test_get_coupon_reads_coupon_property_with_priority():
    subscription = {
        "coupon": {"code": "COUPON12345678"},
        "createdAt": 1636922909,
        "expiresAt": 1669668509,
        "orders": [],
    }

    assert get_coupon(subscription) == "COUPON12345678"


def test_get_coupon_looks_at_last_order_if_no_coupon_property_set():
    subscription = {
        "coupon": None,
        "createdAt": 1636922909,
        "expiresAt": 1669668509,
        "orders": [
            {"coupon": {"code": "COUPON12345678"}, "createdAt": 1637228062},
            {"coupon": None, "createdAt": 1636018061},
        ],
    }

    assert get_coupon(subscription) == "COUPON12345678"


def test_get_coupon_sorts_orders_by_date():
    subscription = {
        "coupon": None,
        "createdAt": 1636922909,
        "expiresAt": 1669668509,
        "orders": [
            {"coupon": None, "createdAt": 1636018061},
            {"coupon": {"code": "COUPON12345678"}, "createdAt": 1637228062},
        ],
    }

    assert get_coupon(subscription) == "COUPON12345678"


def test_get_coupon_looks_at_last_order_only():
    subscription = {
        "coupon": None,
        "createdAt": 1636922909,
        "expiresAt": 1669668509,
        "orders": [
            {"coupon": None, "createdAt": 1637228062},
            {"coupon": {"code": "COUPON12345678"}, "createdAt": 1636018061},
        ],
    }

    assert get_coupon(subscription) is None


def test_get_active_subscription():
    assert get_active_subscription(
        [
            dict(id=1, active=False, activatedAt=123, plan=PLAN_CLUB),
            dict(id=2, active=True, activatedAt=123, plan=PLAN_CLUB),
            dict(id=3, active=False, activatedAt=123, plan=PLAN_CLUB),
        ]
    ) == dict(id=2, active=True, activatedAt=123, plan=PLAN_CLUB)


def test_get_active_subscription_skip_without_plan_group():
    assert get_active_subscription(
        [
            dict(id=1, active=True, activatedAt=123, plan=PLAN_CLUB),
            dict(id=2, active=True, activatedAt=123, plan=PLAN_OTHER),
            dict(id=3, active=False, activatedAt=123, plan=PLAN_CLUB),
        ]
    ) == dict(id=1, active=True, activatedAt=123, plan=PLAN_CLUB)


def test_get_active_subscription_multiple_active():
    with pytest.raises(ValueError):
        get_active_subscription(
            [
                dict(id=1, active=True, activatedAt=123, plan=PLAN_CLUB),
                dict(id=2, active=True, activatedAt=123, plan=PLAN_CLUB),
                dict(id=3, active=False, activatedAt=123, plan=PLAN_CLUB),
            ]
        )


@pytest.mark.parametrize(
    "today, active1, expected",
    [
        (
            date(2023, 8, 10),
            True,
            dict(id=1, active=True, activatedAt=1663146115, plan=PLAN_CLUB),
        ),
        (
            date(2023, 9, 14),
            True,
            dict(id=2, active=True, activatedAt=1694685504, plan=PLAN_CLUB),
        ),
        (
            date(2023, 9, 14),
            False,
            dict(id=2, active=True, activatedAt=1694685504, plan=PLAN_CLUB),
        ),
        (
            date(2023, 9, 15),
            False,
            dict(id=2, active=True, activatedAt=1694685504, plan=PLAN_CLUB),
        ),
        (
            date(2023, 9, 16),
            False,
            dict(id=2, active=True, activatedAt=1694685504, plan=PLAN_CLUB),
        ),
    ],
)
def test_get_active_subscription_multiple_active_but_one_starts_in_the_future(
    today, active1, expected
):
    assert (
        get_active_subscription(
            [
                dict(id=2, active=True, activatedAt=1694685504, plan=PLAN_CLUB),
                dict(id=1, active=active1, activatedAt=1663146115, plan=PLAN_CLUB),
            ],
            today=today,
        )
        == expected
    )


def test_get_active_subscription_no_active():
    with pytest.raises(ValueError):
        get_active_subscription(
            [
                dict(id=1, active=False, activatedAt=123, plan=PLAN_CLUB),
                dict(id=2, active=False, activatedAt=123, plan=PLAN_CLUB),
                dict(id=3, active=False, activatedAt=123, plan=PLAN_CLUB),
            ]
        )


def test_get_active_subscription_no_items():
    with pytest.raises(ValueError):
        get_active_subscription([])


def test_get_expires_at():
    expires_at = get_expires_at(
        [
            dict(id=1, active=True, expiresAt=1663146115, plan=PLAN_CLUB),
            dict(id=2, active=False, expiresAt=1694685504, plan=PLAN_CLUB),
        ]
    )

    assert expires_at == datetime(2022, 9, 14, 9, 1, 55)


def test_get_expires_at_multiple_active_and_one_expires_later():
    expires_at = get_expires_at(
        [
            dict(id=1, active=True, expiresAt=1663146115, plan=PLAN_CLUB),
            dict(id=2, active=True, expiresAt=1694685504, plan=PLAN_CLUB),
        ]
    )

    assert expires_at == datetime(2023, 9, 14, 9, 58, 24)
