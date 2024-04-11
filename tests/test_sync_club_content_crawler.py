import logging
from collections import namedtuple
from datetime import datetime, timedelta, timezone

import pytest

from project.sync.club_content.crawler import get_channel_logger, get_history_after


def test_get_history_after_given_naive_datetime():
    with pytest.raises(ValueError):
        get_history_after(timedelta(days=2), now=datetime(2023, 8, 29))


def test_get_history_after_given_timezone_aware_datetime():
    history_after = get_history_after(
        timedelta(days=2), now=datetime(2023, 8, 30, tzinfo=timezone.utc)
    )

    assert history_after == datetime(2023, 8, 28, tzinfo=timezone.utc)


def test_get_channel_logger():
    logger = logging.getLogger("test_get_channel_logger")
    StubChannel = namedtuple("Channel", ["id"])
    channel = StubChannel(1)
    channel_logger = get_channel_logger(logger, channel)

    assert channel_logger.name == "test_get_channel_logger.1"


def test_get_channel_logger_thread():
    logger = logging.getLogger("test_get_channel_logger")
    StubChannel = namedtuple("Channel", ["id", "parent"])
    channel = StubChannel(1, None)
    thread = StubChannel(2, channel)
    channel_logger = get_channel_logger(logger, thread)

    assert channel_logger.name == "test_get_channel_logger.1.2"
