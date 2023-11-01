from datetime import date, timedelta

import requests

from juniorguru.cli.sync import main as cli
from juniorguru.lib import charts, loggers
from juniorguru.models.base import db
from juniorguru.models.web_usage import WebUsage


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
            f'Fetching analytics from {time_range["start"]} to {time_range["end"]}'
        )
        for slug, pages in PRODUCTS.items():
            logger.debug(f'Fetching analytics for {slug!r}: {", ".join(pages)}')
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
            starts_on = date.fromisoformat(time_range["start"])
            logger.info(
                f'Product {slug!r} got {data["pageviews"]} pageviews on {starts_on:%Y-%m}'
            )
            WebUsage.create(
                product_slug=slug,
                month_starts_on=starts_on,
                pageviews=data["pageviews"],
            )
