from datetime import date, timedelta

import requests

from jg.coop.cli.sync import main as cli
from jg.coop.lib import charts, loggers
from jg.coop.lib.cache import cache
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
    "podcast": [
        "/podcast",
        "/podcast/",
    ],
}

MONTHS_RANGE = 12


logger = loggers.from_path(__file__)


@cli.sync_command()
@db.connection_context()
def main():
    WebUsage.drop_table()
    WebUsage.create_table()

    date_to = date.today()
    date_from = date_to - timedelta(days=30 * MONTHS_RANGE)
    time_ranges = [
        dict(start=month.replace(day=1).isoformat(), end=month.isoformat())
        for month in charts.generate_months(date_from, date_to)
    ][:MONTHS_RANGE]

    for time_range in time_ranges:
        logger.debug(
            f"Fetching analytics from {time_range['start']} to {time_range['end']}"
        )
        for slug, pages in PRODUCTS.items():
            logger.debug(f"Fetching analytics for {slug!r}: {', '.join(pages)}")
            pageviews = fetch_analytics(pages, time_range)
            starts_on = date.fromisoformat(time_range["start"])
            logger.info(
                f"Product {slug!r} got {pageviews} pageviews on {starts_on:%Y-%m}"
            )
            WebUsage.create(
                product_slug=slug,
                month_starts_on=starts_on,
                pageviews=pageviews,
            )


@cache(expire=timedelta(days=40), tag="web-usage")
def fetch_analytics(pages: list[str], time_range: dict[str, str]) -> int:
    params = dict(
        version=5,
        fields="pageviews",
        info="false",
        pages=",".join(pages),
        **time_range,
    )
    response = requests.get(
        "https://simpleanalytics.com/junior.guru.json", params=params
    )
    response.raise_for_status()
    data = response.json()
    return data["pageviews"]
