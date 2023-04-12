from datetime import datetime, timedelta, timezone

import pytest

from juniorguru.sync.club_content.crawler import get_history_after


def test_get_history_after_given_naive_datetime():
    with pytest.raises(ValueError):
        get_history_after(timedelta(days=2), now=datetime(2023, 8, 29))


def test_get_history_after_given_timezone_aware_datetime():
    history_after = get_history_after(timedelta(days=2), now=datetime(2023, 8, 30, tzinfo=timezone.utc))

    assert history_after == datetime(2023, 8, 28, tzinfo=timezone.utc)
