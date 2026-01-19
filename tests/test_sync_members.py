from datetime import date, datetime

import pytest

from jg.coop.models.club import SubscriptionType
from jg.coop.sync.members import (
    get_active_subscription,
    get_coupon,
    get_expires_at,
    get_subscription_type,
    had_quit,
    had_signup,
    had_trial,
)


PLAN_CLUB = {
    "name": "Členství v klubu",
    "planGroup": {"name": "abc"},
    "intervalUnit": "month",
    "additionalMemberPriceCents": None,
}

PLAN_GROUP = {
    "name": "Skupinka",
    "planGroup": None,
    "intervalUnit": "year",
    "additionalMemberPriceCents": 0,
}


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
    subscription = get_active_subscription(
        [
            {
                "id": 1,
                "active": False,
                "activatedAt": 1725177843,
                "trialEndAt": None,
                "plan": PLAN_CLUB,
                "coupon": None,
                "orders": [{"coupon": None, "createdAt": 100}],
            },
            {
                "id": 2,
                "active": True,
                "activatedAt": 1725177843,
                "trialEndAt": None,
                "plan": PLAN_CLUB,
                "coupon": None,
                "orders": [{"coupon": None, "createdAt": 100}],
            },
            {
                "id": 3,
                "active": False,
                "activatedAt": 1725177843,
                "trialEndAt": None,
                "plan": PLAN_CLUB,
                "coupon": None,
                "orders": [{"coupon": None, "createdAt": 100}],
            },
        ]
    )

    assert subscription["id"] == 2


def test_get_active_subscription_dont_skip_group_plans():
    subscription = get_active_subscription(
        [
            {
                "id": 1,
                "active": True,
                "activatedAt": 1725177843,
                "trialEndAt": None,
                "plan": PLAN_GROUP,
                "coupon": None,
                "orders": [{"coupon": None, "createdAt": 100}],
            },
            {
                "id": 2,
                "active": False,
                "activatedAt": 1725177843,
                "trialEndAt": None,
                "plan": PLAN_GROUP,
                "coupon": None,
                "orders": [{"coupon": None, "createdAt": 100}],
            },
        ]
    )

    assert subscription["id"] == 1


def test_get_active_subscription_multiple_active():
    with pytest.raises(ValueError):
        get_active_subscription(
            [
                {
                    "id": 1,
                    "active": True,
                    "activatedAt": 1725177843,
                    "trialEndAt": None,
                    "plan": PLAN_CLUB,
                    "coupon": None,
                    "orders": [{"coupon": None, "createdAt": 100}],
                },
                {
                    "id": 2,
                    "active": True,
                    "activatedAt": 1725177843,
                    "trialEndAt": None,
                    "plan": PLAN_CLUB,
                    "coupon": None,
                    "orders": [{"coupon": None, "createdAt": 100}],
                },
                {
                    "id": 3,
                    "active": False,
                    "activatedAt": 1725177843,
                    "trialEndAt": None,
                    "plan": PLAN_CLUB,
                    "coupon": None,
                    "orders": [{"coupon": None, "createdAt": 100}],
                },
            ]
        )


def test_get_active_subscription_multiple_active_tolerates_finaid_together_with_group_plan():
    subscription = get_active_subscription(
        [
            {
                "id": 1,
                "active": True,
                "activatedAt": 1725177843,
                "trialEndAt": None,
                "plan": PLAN_GROUP,
                "coupon": None,
                "orders": [{"coupon": None, "createdAt": 100}],
            },
            {
                "id": 2,
                "active": True,
                "activatedAt": 1725177843,
                "trialEndAt": None,
                "plan": PLAN_CLUB,
                "coupon": None,
                "orders": [{"coupon": {"code": "FINAID12345678"}, "createdAt": 100}],
            },
            {
                "id": 3,
                "active": False,
                "activatedAt": 1725177843,
                "trialEndAt": None,
                "plan": PLAN_CLUB,
                "coupon": None,
                "orders": [{"coupon": None, "createdAt": 100}],
            },
        ]
    )

    assert subscription["id"] == 1


@pytest.mark.parametrize(
    "today, active1, expected_id",
    [
        (date(2023, 8, 10), True, 1),
        (date(2023, 9, 14), True, 2),
        (date(2023, 9, 14), False, 2),
        (date(2023, 9, 15), False, 2),
        (date(2023, 9, 16), False, 2),
    ],
)
def test_get_active_subscription_multiple_active_but_one_starts_in_the_future(
    today, active1, expected_id
):
    subscription = get_active_subscription(
        [
            {
                "id": 2,
                "active": True,
                "activatedAt": 1694685504,
                "trialEndAt": None,
                "plan": PLAN_CLUB,
                "coupon": None,
                "orders": [{"coupon": None, "createdAt": 100}],
            },
            {
                "id": 1,
                "active": active1,
                "activatedAt": 1663146115,
                "trialEndAt": None,
                "plan": PLAN_CLUB,
                "coupon": None,
                "orders": [{"coupon": None, "createdAt": 100}],
            },
        ],
        today=today,
    )

    assert subscription["id"] == expected_id


def test_get_active_subscription_no_active():
    with pytest.raises(ValueError):
        get_active_subscription(
            [
                {
                    "id": 1,
                    "active": False,
                    "activatedAt": 1725177843,
                    "trialEndAt": None,
                    "plan": PLAN_CLUB,
                    "coupon": None,
                    "orders": [{"coupon": None, "createdAt": 100}],
                },
                {
                    "id": 2,
                    "active": False,
                    "activatedAt": 1725177843,
                    "trialEndAt": None,
                    "plan": PLAN_CLUB,
                    "coupon": None,
                    "orders": [{"coupon": None, "createdAt": 100}],
                },
                {
                    "id": 3,
                    "active": False,
                    "activatedAt": 1725177843,
                    "trialEndAt": None,
                    "plan": PLAN_CLUB,
                    "coupon": None,
                    "orders": [{"coupon": None, "createdAt": 100}],
                },
            ]
        )


def test_get_active_subscription_no_items():
    with pytest.raises(ValueError):
        get_active_subscription([])


def test_get_expires_at():
    expires_at = get_expires_at(
        [
            {
                "id": 1,
                "active": True,
                "expiresAt": 1663146115,
                "plan": PLAN_CLUB,
                "coupon": None,
            },
            {
                "id": 2,
                "active": False,
                "expiresAt": 1694685504,
                "plan": PLAN_CLUB,
                "coupon": None,
            },
        ]
    )

    assert expires_at == datetime(2022, 9, 14, 9, 1, 55)


def test_get_expires_at_multiple_active_and_one_expires_later():
    expires_at = get_expires_at(
        [
            {
                "id": 1,
                "active": True,
                "expiresAt": 1663146115,
                "plan": PLAN_CLUB,
                "coupon": None,
            },
            {
                "id": 2,
                "active": True,
                "expiresAt": 1694685504,
                "plan": PLAN_CLUB,
                "coupon": None,
            },
        ]
    )

    assert expires_at == datetime(2023, 9, 14, 9, 58, 24)


def test_get_subscription_type_recognizes_free():
    subscription = {
        "id": "123",
        "active": True,
        "activatedAt": 1618917537,
        "trialEndAt": 1620127137,
        "expiresAt": 1736519540,
        "orders": [
            {"createdAt": 1704897711, "coupon": {"code": "THANKYOU123"}},
            {"createdAt": 1651663309, "coupon": {"code": "THANKYOU123"}},
            {"createdAt": 1620127422, "coupon": {"code": "THANKYOU123"}},
            {"createdAt": 1618917537, "coupon": None},
        ],
        "plan": {
            "name": "Roční členství v klubu",
            "intervalUnit": "year",
            "forSale": True,
            "additionalMemberPriceCents": None,
            "planGroup": {"name": "Členství v klubu"},
        },
        "coupon": {"code": "THANKYOU123"},
    }

    assert get_subscription_type(subscription) == SubscriptionType.FREE


def test_get_subscription_type_recognizes_finaid():
    subscription = {
        "id": "123",
        "active": True,
        "activatedAt": 1713203206,
        "trialEndAt": 1712853626,
        "expiresAt": 1745922462,
        "orders": [
            {"createdAt": 1713203206, "coupon": None},
            {"createdAt": 1711644026, "coupon": None},
        ],
        "plan": {
            "name": "Roční členství v klubu",
            "intervalUnit": "year",
            "forSale": True,
            "additionalMemberPriceCents": None,
            "planGroup": {"name": "Členství v klubu"},
        },
        "coupon": {"code": "FINAID123"},
    }

    assert get_subscription_type(subscription) == SubscriptionType.FINAID


def test_get_subscription_type_recognizes_trial():
    subscription = {
        "id": "123",
        "active": True,
        "activatedAt": 1720707511,
        "trialEndAt": 1721917111,
        "expiresAt": 1721917111,
        "coupon": None,
        "orders": [{"createdAt": 1720707511, "coupon": None}],
        "plan": {
            "name": "Členství v klubu",
            "intervalUnit": "month",
            "forSale": True,
            "additionalMemberPriceCents": None,
            "planGroup": {"name": "Členství v klubu"},
        },
    }

    assert (
        get_subscription_type(subscription, today=date(2024, 7, 12))
        == SubscriptionType.TRIAL
    )


@pytest.mark.parametrize("member_price_cents", [0, 10000])
def test_get_subscription_type_recognizes_sponsor(member_price_cents: int):
    subscription = {
        "id": "123",
        "active": True,
        "activatedAt": 1720169340,
        "trialEndAt": None,
        "expiresAt": 1743465600,
        "coupon": None,
        "orders": [{"createdAt": 1720169340, "coupon": None}],
        "plan": {
            "name": "Tarif „Poskytujeme kurzy“",
            "intervalUnit": "year",
            "forSale": True,
            "additionalMemberPriceCents": member_price_cents,
            "planGroup": {"name": "Skupinové členství v klubu"},
        },
    }

    assert get_subscription_type(subscription) == SubscriptionType.SPONSOR


def test_get_subscription_type_recognizes_partner():
    subscription = {
        "id": "123",
        "active": True,
        "activatedAt": 1720171705,
        "trialEndAt": None,
        "expiresAt": 1752278400,
        "coupon": None,
        "orders": [{"createdAt": 1720171705, "coupon": None}],
        "plan": {
            "name": "Partnerství",
            "intervalUnit": "year",
            "forSale": False,
            "additionalMemberPriceCents": 0,
            "planGroup": None,
        },
    }

    assert get_subscription_type(subscription) == SubscriptionType.PARTNER


def test_get_subscription_type_recognizes_partner_with_non_standard_plan():
    subscription = {
        "id": "123",
        "active": True,
        "activatedAt": 1720173036,
        "trialEndAt": None,
        "expiresAt": 1752278400,
        "coupon": None,
        "orders": [{"createdAt": 1720173036, "coupon": None}],
        "plan": {
            "name": "Mentoring „CoreSkill“",
            "intervalUnit": "month",
            "forSale": False,
            "additionalMemberPriceCents": 0,
            "planGroup": None,
        },
    }

    assert get_subscription_type(subscription) == SubscriptionType.PARTNER


def test_get_subscription_type_recognizes_monthly():
    subscription = {
        "id": "123",
        "active": True,
        "activatedAt": 1713278659,
        "trialEndAt": 1714488259,
        "expiresAt": 1722350659,
        "coupon": None,
        "orders": [
            {"createdAt": 1719759085, "coupon": None},
            {"createdAt": 1717080679, "coupon": None},
            {"createdAt": 1714488664, "coupon": None},
            {"createdAt": 1713278659, "coupon": None},
        ],
        "plan": {
            "name": "Členství v klubu",
            "intervalUnit": "month",
            "forSale": True,
            "additionalMemberPriceCents": None,
            "planGroup": {"name": "Členství v klubu"},
        },
    }

    assert get_subscription_type(subscription) == SubscriptionType.MONTHLY


def test_get_subscription_type_recognizes_yearly():
    subscription = {
        "id": "123",
        "active": True,
        "activatedAt": 1692872000,
        "trialEndAt": 1694081600,
        "expiresAt": 1725704000,
        "coupon": None,
        "orders": [
            {"createdAt": 1694082165, "coupon": None},
            {"createdAt": 1692872000, "coupon": None},
        ],
        "plan": {
            "name": "Roční členství v klubu",
            "intervalUnit": "year",
            "forSale": True,
            "additionalMemberPriceCents": None,
            "planGroup": {"name": "Členství v klubu"},
        },
    }

    assert get_subscription_type(subscription) == SubscriptionType.YEARLY


def test_bug():
    today = date(2024, 10, 7)
    subscription = {
        "id": "3831901",
        "active": True,
        "activatedAt": 1728281556,
        "trialStartAt": 1728281556,
        "trialEndAt": 1729491156,
        "expiresAt": 1729491156,
        "coupon": None,
        "orders": [{"createdAt": 1728281556, "coupon": None}],
        "plan": {
            "name": "Členství v klubu",
            "intervalUnit": "month",
            "forSale": True,
            "additionalMemberPriceCents": None,
            "planGroup": {"name": "Členství v klubu"},
        },
    }

    assert get_subscription_type(subscription, today) == SubscriptionType.TRIAL


def test_is_signup():
    member = {
        "totalSpendCents": 0,
        "subscriptions": [
            {
                "id": "123",
                "active": True,
                "activatedAt": 1719220724,
                "trialStartAt": 1719220724,
                "trialEndAt": 1720430324,
                "expiresAt": 1723108724,
                "coupon": None,
                "orders": [
                    {"createdAt": 1720430507, "coupon": None},
                    {"createdAt": 1719220724, "coupon": None},
                ],
                "plan": {
                    "name": "Členství v klubu",
                    "intervalUnit": "month",
                    "forSale": True,
                    "additionalMemberPriceCents": None,
                    "planGroup": {"name": "Členství v klubu"},
                },
            }
        ],
    }

    assert had_signup(member, date(2024, 7, 1), date(2024, 7, 31)) is True


def test_is_trial():
    member = {
        "totalSpendCents": 0,
        "subscriptions": [
            {
                "id": "123",
                "active": True,
                "activatedAt": 1720784300,
                "trialStartAt": 1720784300,
                "trialEndAt": 1721993900,
                "expiresAt": 1721993900,
                "coupon": None,
                "orders": [{"createdAt": 1720784300, "coupon": None}],
                "plan": {
                    "name": "Členství v klubu",
                    "intervalUnit": "month",
                    "forSale": True,
                    "additionalMemberPriceCents": None,
                    "planGroup": {"name": "Členství v klubu"},
                },
            }
        ],
    }

    assert had_trial(member, date(2024, 7, 1), date(2024, 7, 31)) is True


def test_is_quit():
    member = {
        "totalSpendCents": 39800,
        "subscriptions": [
            {
                "id": "123",
                "active": False,
                "activatedAt": None,
                "trialStartAt": 1713805776,
                "trialEndAt": 1715015376,
                "expiresAt": 1720285776,
                "coupon": None,
                "orders": [
                    {"createdAt": 1717693904, "coupon": None},
                    {"createdAt": 1715015470, "coupon": None},
                    {"createdAt": 1713805776, "coupon": None},
                ],
                "plan": {
                    "name": "Členství v klubu",
                    "intervalUnit": "month",
                    "forSale": True,
                    "additionalMemberPriceCents": None,
                    "planGroup": {"name": "Členství v klubu"},
                },
            }
        ],
    }

    assert had_quit(member, date(2024, 7, 1), date(2024, 7, 31)) is True
