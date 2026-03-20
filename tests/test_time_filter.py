from datetime import date

import pytest

from jg.coop.sync.jobs_scraped.pipelines.time_filter import DropItem, process


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "posted_on, today, days",
    [
        pytest.param(
            "2026-03-18",
            date(2026, 3, 20),
            1,
            id="plain date, before threshold",
        ),
        pytest.param(
            "2026-03-18T10:00:00.000Z",
            date(2026, 3, 20),
            1,
            id="ISO with time, before threshold",
        ),
        pytest.param(
            "2026-03-17",
            date(2026, 3, 20),
            2,
            id="plain date, before threshold (2 days)",
        ),
        pytest.param(
            "2026-03-17T23:59:59.000Z",
            date(2026, 3, 20),
            2,
            id="ISO with time, before threshold (2 days)",
        ),
    ],
)
async def test_process_should_drop(posted_on: str, today: date, days: int) -> None:
    with pytest.raises(DropItem):
        await process({"posted_on": posted_on}, today=today, days=days)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "posted_on, today, days",
    [
        pytest.param(
            "2026-03-19",
            date(2026, 3, 20),
            1,
            id="plain date, on threshold",
        ),
        pytest.param(
            "2026-03-19T10:54:28.000Z",
            date(2026, 3, 20),
            1,
            id="ISO with time, on threshold",
        ),
        pytest.param(
            "2026-03-20", date(2026, 3, 20), 1, id="plain date, after threshold"
        ),
        pytest.param(
            "2026-03-20T10:54:28.000Z",
            date(2026, 3, 20),
            1,
            id="ISO with time, after threshold",
        ),
        pytest.param(
            "2026-03-18", date(2026, 3, 20), 2, id="plain date, on threshold (2 days)"
        ),
        pytest.param(
            "2026-03-18T23:59:59.000Z",
            date(2026, 3, 20),
            2,
            id="ISO with time, on threshold (2 days)",
        ),
        pytest.param(
            "2026-03-19",
            date(2026, 3, 20),
            2,
            id="plain date, after threshold (2 days)",
        ),
        pytest.param(
            "2026-03-19T00:00:00.000Z",
            date(2026, 3, 20),
            2,
            id="ISO with time, after threshold (2 days)",
        ),
    ],
)
async def test_process_should_not_drop(posted_on: str, today: date, days: int) -> None:
    item = {"posted_on": posted_on}

    assert (await process(item, today=today, days=days)) == item
