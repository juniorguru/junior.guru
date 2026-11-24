import json
from datetime import UTC, date, datetime, time, timedelta
from fnmatch import fnmatchcase
from operator import itemgetter
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import click
import httpx2
from tenacity import retry_if_exception_type

from jg.coop.cli.sync import main as cli
from jg.coop.lib import charts, loggers
from jg.coop.lib.retrying import retry
from jg.coop.models.base import db
from jg.coop.models.web_usage import WebUsage


PRODUCTS = {
    "total": [
        "*",
    ],
    "home": [
        "/",
    ],
    "club": [
        "/club",
        "/club/",
    ],
    "handbook": [
        "/handbook",
        "/handbook/",
        "/handbook/*",
    ],
    "courses": [
        "/courses",
        "/courses/",
        "/courses/*",
    ],
    "jobs": [
        "/jobs",
        "/jobs/",
        "/jobs/*",
    ],
    "candidates": [
        "/candidates",
        "/candidates/",
    ],
    "inspiration": [
        "/news",
        "/news/",
        "/podcast",
        "/podcast/",
        "/events",
        "/events/",
        "/stories",
        "/stories/",
        "/stories/*",
        "/wisdom",
        "/wisdom/",
    ],
}

MONTHS_RANGE = 12

API_URL = "https://simpleanalytics.com/junior.guru.json"

API_VERSION = 6

API_TIMEZONE = ZoneInfo("Europe/Prague")

# Maximum the API allows, a month has a few hundred distinct paths at most
PAGES_LIMIT = 1000

# Simple Analytics can take several seconds to generate the stats
TIMEOUT = 60


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option(
    "--data-dir",
    default=Path("src/jg/coop/data/web_usage"),
    type=click.Path(path_type=Path, file_okay=False, writable=True),
)
@db.connection_context()
def main(data_dir: Path):
    data_dir.mkdir(parents=True, exist_ok=True)
    months = get_months(date.today(), MONTHS_RANGE)
    existing_months = {
        date.fromisoformat(f"{path.stem}-01") for path in data_dir.glob("*.jsonl")
    }
    for month in get_months_to_sync(months, existing_months):
        logger.info(f"Fetching pageviews for {month:%Y-%m}")
        data = fetch_pages(month, charts.next_month(month))
        pages = parse_pages(data, month, charts.next_month(month))
        path = data_dir / f"{month:%Y-%m}.jsonl"
        path.write_text(serialize_pages(pages))
        logger.info(f"Saved {len(pages)} pages to {path}")

    WebUsage.drop_table()
    WebUsage.create_table()
    for month in months:
        path = data_dir / f"{month:%Y-%m}.jsonl"
        pages = deserialize_pages(path.read_text())
        for slug, pageviews in aggregate_products(pages, PRODUCTS).items():
            logger.info(f"Product {slug!r} got {pageviews} pageviews on {month:%Y-%m}")
            WebUsage.create(
                product_slug=slug,
                month_starts_on=month,
                pageviews=pageviews,
            )


@retry(retry=retry_if_exception_type(httpx2.HTTPError))
def fetch_pages(start: date, end: date) -> dict[str, Any]:
    response = httpx2.get(
        API_URL,
        params={
            "version": API_VERSION,
            "info": "false",
            "fields": "pageviews,pages",
            "limit": PAGES_LIMIT,
            "start": start.isoformat(),
            "end": end.isoformat(),
        },
        follow_redirects=True,
        timeout=TIMEOUT,
    )
    logger.debug(f"API URL: {response.url}")
    response.raise_for_status()
    return response.json()


def get_months(today: date, months_range: int) -> list[date]:
    """
    Returns first days of the given number of complete months preceding
    the current one, oldest first
    """
    months = [charts.previous_month(today).replace(day=1)]
    while len(months) < months_range:
        months.insert(0, charts.previous_month(months[0]).replace(day=1))
    return months


def get_months_to_sync(months: list[date], existing_months: set[date]) -> list[date]:
    return [month for month in months if month not in existing_months]


def parse_pages(data: dict[str, Any], start: date, end: date) -> list[dict[str, Any]]:
    """
    Turns the API response into a list of pages with their pageviews and
    checks the list is complete, as the pageviews of products are computed
    from it

    The end date is exclusive, which is how the Simple Analytics API treats it.
    """
    if not data.get("ok"):
        raise ValueError(f"Unexpected API response: {data!r}")
    if (actual_range := parse_range(data)) != (expected_range := (start, end)):
        raise ValueError(
            f"API returned range {actual_range}, expected {expected_range}"
        )
    if len(data["pages"]) >= PAGES_LIMIT:
        raise ValueError(f"API returned {PAGES_LIMIT} pages, the list may be truncated")
    pages = [
        {"page": page["value"], "pageviews": page["pageviews"]}
        for page in data["pages"]
    ]
    if (pages_total := sum(map(itemgetter("pageviews"), pages))) != data["pageviews"]:
        raise ValueError(
            f"Pages sum up to {pages_total} pageviews, but the total is {data['pageviews']}"
        )
    return pages


def parse_range(data: dict[str, Any]) -> tuple[date, date]:
    """Returns the echoed start and exclusive end of the API response as local dates"""
    start = parse_api_datetime(data["start"])
    end = parse_api_datetime(data["end"])
    if start.time() != time.min or end.time() != time.max.replace(microsecond=999000):
        raise ValueError(f"API returned range not aligned to days: {start} – {end}")
    return start.date(), end.date() + timedelta(days=1)


def parse_api_datetime(value: str) -> datetime:
    return (
        datetime.fromisoformat(value)
        .replace(tzinfo=UTC)
        .astimezone(API_TIMEZONE)
        .replace(tzinfo=None)
    )


def aggregate_products(
    pages: list[dict[str, Any]], products: dict[str, list[str]]
) -> dict[str, int]:
    return {
        slug: sum(
            page["pageviews"]
            for page in pages
            if any(fnmatchcase(page["page"], pattern) for pattern in patterns)
        )
        for slug, patterns in products.items()
    }


def serialize_pages(pages: list[dict[str, Any]]) -> str:
    return "".join(
        f"{json.dumps(page, ensure_ascii=False)}\n"
        for page in sorted(pages, key=itemgetter("page"))
    )


def deserialize_pages(text: str) -> list[dict[str, Any]]:
    return [json.loads(line) for line in text.splitlines() if line.strip()]
