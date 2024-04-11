from collections import namedtuple
from datetime import date

import pytest

from coop.sync.core_members_discount import (
    get_discount_info,
    is_recent_reminder,
    repr_members,
)


@pytest.mark.parametrize(
    "created_at, expected",
    [
        (date(2023, 8, 23), True),
        (date(2023, 8, 22), True),
        (date(2023, 8, 21), True),
        (date(2023, 8, 20), True),
        (date(2023, 8, 19), False),
        (date(2023, 8, 18), False),
        (date(2023, 1, 1), False),
    ],
)
def test_is_recent_reminder(created_at: date, expected: bool):
    today = date(2023, 8, 23)
    StubMessage = namedtuple("Message", ["created_at"])
    message = StubMessage(created_at=created_at)

    assert is_recent_reminder(message, today=today, days=3) is expected


def test_is_recent_reminder_returns_false_when_given_no_message():
    assert is_recent_reminder(None) is False


def test_repr_members_sorts_by_lowercased():
    StubMember = namedtuple("Member", ["display_name"])
    members = [
        StubMember(display_name="Bob"),
        StubMember(display_name="Alice"),
        StubMember(display_name="abigail"),
        StubMember(display_name="ashley"),
    ]

    assert repr_members(members) == "abigail, Alice, ashley, Bob"


def test_get_discount_info():
    coupons = [
        {
            "amountOffCents": 10000,
            "code": "ABCD1234567",
            "id": "1",
            "isPercentage": True,
        },
        {
            "amountOffCents": 1000,
            "code": "COREMEMBER1234567",
            "id": "2",
            "isPercentage": True,
        },
        {
            "amountOffCents": 10000,
            "code": "EFGH1234567",
            "id": "3",
            "isPercentage": True,
        },
    ]

    assert get_discount_info(coupons, "coremember") == {
        "coupon": "COREMEMBER1234567",
        "ptc_off": 10,
    }
