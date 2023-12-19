from datetime import date, datetime

import pytest

from juniorguru.models.subscription import SubscriptionActivityType
from juniorguru.sync.subscriptions import (
    activities_from_subscription,
    get_coupon_slug,
    get_timestamp,
)


PLAN_GROUP = dict(planGroup=dict(name='abc'))


def test_activities_from_subscription():
    subscription = {
        "active": True,
        "coupon": {"code": "THANKYOU1234567890"},
        "createdAt": 1634013431,
        "activatedAt": 1634013431,
        "expiresAt": 1701970564,
        "id": "123456",
        "member": {"fullName": "Keira Heart", "id": "2782496"},
        "orders": [
            {"coupon": None, "createdAt": 1670360425},
            {"coupon": {"code": "THANKYOU1234567890"}, "createdAt": 1635223064},
            {"coupon": None, "createdAt": 1634013431},
        ],
        "plan": {"intervalUnit": "year", 'planGroup': PLAN_GROUP},
        "trialEndAt": 1635223031,
        "trialStartAt": 1634013431,
    }
    assert list(activities_from_subscription(subscription)) == [
        {
            "account_id": 2782496,
            "type": SubscriptionActivityType.ORDER,
            "happened_on": date(2021, 10, 12),
            "happened_at": datetime(2021, 10, 12, 4, 37, 11),
            "subscription_interval": "year",
            "order_coupon_slug": "thankyou",
        },
        {
            "account_id": 2782496,
            "type": SubscriptionActivityType.DEACTIVATION,
            "happened_on": date(2023, 12, 7),
            "happened_at": datetime(2023, 12, 7, 17, 36, 4),
            "subscription_interval": "year",
            "order_coupon_slug": "thankyou",
        },
        {
            "account_id": 2782496,
            "type": SubscriptionActivityType.ORDER,
            "happened_on": date(2021, 10, 12),
            "happened_at": datetime(2021, 10, 12, 4, 37, 11),
            "subscription_interval": "year",
            "order_coupon_slug": "thankyou",
        },
        {
            "account_id": 2782496,
            "type": SubscriptionActivityType.TRIAL_START,
            "happened_on": date(2021, 10, 12),
            "happened_at": datetime(2021, 10, 12, 4, 37, 11),
            "subscription_interval": "year",
            "order_coupon_slug": "thankyou",
        },
        {
            "account_id": 2782496,
            "type": SubscriptionActivityType.TRIAL_END,
            "happened_on": date(2021, 10, 26),
            "happened_at": datetime(2021, 10, 26, 4, 37, 11),
            "subscription_interval": "year",
            "order_coupon_slug": "thankyou",
        },
        {
            "account_id": 2782496,
            "type": SubscriptionActivityType.ORDER,
            "happened_on": date(2022, 12, 6),
            "happened_at": datetime(2022, 12, 6, 21, 0, 25),
            "subscription_interval": "year",
            "order_coupon_slug": "thankyou",
        },
        {
            "account_id": 2782496,
            "type": SubscriptionActivityType.ORDER,
            "happened_on": date(2021, 10, 26),
            "happened_at": datetime(2021, 10, 26, 4, 37, 44),
            "subscription_interval": "year",
            "order_coupon_slug": "thankyou",
        },
        {
            "account_id": 2782496,
            "type": SubscriptionActivityType.ORDER,
            "happened_on": date(2021, 10, 12),
            "happened_at": datetime(2021, 10, 12, 4, 37, 11),
            "subscription_interval": "year",
            "order_coupon_slug": None,
        },
    ]


@pytest.mark.parametrize(
    "coupon_data, expected",
    [
        ({"code": "THANKYOU1234567890"}, "thankyou"),
        ({"code": None}, None),
        (None, None),
    ],
)
def test_get_coupon_slug(coupon_data, expected):
    assert get_coupon_slug(coupon_data) == expected


def test_get_timestamp():
    assert get_timestamp(date(2021, 10, 12)) == 1633996800
