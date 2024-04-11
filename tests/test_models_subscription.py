from datetime import date, datetime

import pytest

from jg.core.models.subscription import SubscriptionActivity

from testing_utils import prepare_test_db


def create_activity(
    account_id: int, type: str, happened_at: datetime
) -> SubscriptionActivity:
    return SubscriptionActivity.create(
        account_id=account_id,
        type=type,
        account_has_feminine_name=True,
        happened_at=happened_at,
        happened_on=happened_at.date(),
    )


@pytest.fixture
def test_db():
    yield from prepare_test_db([SubscriptionActivity])


def test_account_subscribed_at(test_db):
    create_activity(1, "order", datetime(2023, 7, 17))
    create_activity(1, "order", datetime(2023, 6, 17))
    create_activity(1, "order", datetime(2023, 5, 17))
    create_activity(1, "deactivation", datetime(2023, 4, 10))
    create_activity(1, "order", datetime(2023, 3, 9))
    create_activity(1, "trial_end", datetime(2023, 3, 8))
    create_activity(1, "order", datetime(2023, 2, 22))
    create_activity(1, "trial_start", datetime(2023, 2, 22))

    assert SubscriptionActivity.account_subscribed_at(1) == datetime(2023, 2, 22)


def test_account_subscribed_days(test_db):
    today = date.today()
    create_activity(1, "trial_start", datetime(2023, 2, 22))
    create_activity(1, "order", datetime(2023, 2, 22))
    create_activity(1, "trial_end", datetime(2023, 3, 8))
    create_activity(1, "order", datetime(2023, 3, 9))
    create_activity(1, "deactivation", datetime(2023, 4, 10))
    create_activity(1, "order", datetime(2023, 5, 17))
    create_activity(1, "order", datetime(2023, 6, 17))
    create_activity(1, "order", datetime(2023, 7, 17))

    assert SubscriptionActivity.account_subscribed_days(1, today=today) == (
        (date(2023, 4, 10) - date(2023, 2, 22)).days + (today - date(2023, 5, 17)).days
    )


def test_account_subscribed_days_duplicate_deactivation(test_db):
    today = date.today()
    create_activity(1, "order", datetime(2021, 3, 4))
    create_activity(1, "order", datetime(2021, 3, 18))
    create_activity(1, "order", datetime(2022, 3, 18))
    create_activity(1, "order", datetime(2023, 1, 10))
    create_activity(1, "trial_start", datetime(2023, 1, 10))
    create_activity(1, "trial_end", datetime(2023, 1, 24))
    create_activity(1, "order", datetime(2023, 1, 24))
    create_activity(1, "deactivation", datetime(2023, 1, 31))
    create_activity(1, "deactivation", datetime(2023, 2, 24))

    assert SubscriptionActivity.account_subscribed_days(1, today=today) == (
        (date(2023, 1, 31) - date(2021, 3, 4)).days
    )
