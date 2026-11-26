import asyncio
import logging
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from jg.coop.sync.club_content import crawler
from jg.coop.sync.club_content.crawler import (
    get_channel_logger,
    get_history_after,
    join_queue_after,
)


def test_get_history_after_given_naive_datetime():
    with pytest.raises(ValueError):
        get_history_after(timedelta(days=2), now=datetime(2023, 8, 29))


def test_get_history_after_given_timezone_aware_datetime():
    history_after = get_history_after(
        timedelta(days=2), now=datetime(2023, 8, 30, tzinfo=UTC)
    )

    assert history_after == datetime(2023, 8, 28, tzinfo=UTC)


def test_get_channel_logger():
    logger = logging.getLogger("test_get_channel_logger")
    channel = SimpleNamespace(id=1)
    channel_logger = get_channel_logger(logger, channel)

    assert channel_logger.name == "test_get_channel_logger.1"


def test_get_channel_logger_thread():
    logger = logging.getLogger("test_get_channel_logger")
    channel = SimpleNamespace(id=1, parent=None)
    thread = SimpleNamespace(id=2, parent=channel)
    channel_logger = get_channel_logger(logger, thread)

    assert channel_logger.name == "test_get_channel_logger.1.2"


@pytest.mark.asyncio
async def test_join_queue_after_waits_for_producer():
    queue = asyncio.Queue()
    producer_release = asyncio.Event()

    async def producer():
        await producer_release.wait()
        queue.put_nowait("item")

    producer_task = asyncio.create_task(producer())
    join_task = asyncio.create_task(join_queue_after(producer_task, queue))
    await asyncio.sleep(0)  # empty queue would be joined immediately

    assert not join_task.done()

    producer_release.set()
    await producer_task
    queue.get_nowait()
    queue.task_done()
    await join_task


@pytest.mark.asyncio
async def test_crawl_dm_channels_opens_channels_one_by_one(monkeypatch):
    in_progress = 0
    max_in_progress = 0

    async def fake_crawl_dm_channel(queue, member):
        nonlocal in_progress, max_in_progress
        in_progress += 1
        max_in_progress = max(max_in_progress, in_progress)
        await asyncio.sleep(0)
        in_progress -= 1

    monkeypatch.setattr(crawler, "crawl_dm_channel", fake_crawl_dm_channel)
    await crawler.crawl_dm_channels(asyncio.Queue(), [object()] * 5)

    assert max_in_progress == 1
