import calendar
import json
from collections.abc import Iterable
from datetime import date, timedelta
from operator import itemgetter
from pathlib import Path
from typing import Any

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import google_api, loggers


logger = loggers.from_path(__file__)


SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

SITE_DOMAIN = "junior.guru"

SITE_ORIGIN = f"https://{SITE_DOMAIN}/"

LOOKBACK_DAYS = 600

ROW_LIMIT = 25_000

MIN_IMPRESSIONS = 10

REPORTS = {
    "pages": ["page"],
    "queries": ["page", "query"],
}


@cli.sync_command()
@click.option(
    "--data-dir",
    default=Path("src/jg/coop/data/search_console"),
    type=click.Path(path_type=Path, file_okay=False, writable=True),
)
@click.option("--site-url")
def main(data_dir: Path, site_url: str | None) -> None:
    client = google_api.get_client("searchconsole", "v1", scopes=SCOPES)

    if not site_url:
        response = client.sites().list().execute()
        site_url = pick_site_url(
            [entry["siteUrl"] for entry in response.get("siteEntry", [])]
        )
    logger.info(f"Site: {site_url}")

    available_dates = fetch_available_dates(client, site_url)
    months = get_complete_months(available_dates)
    if not months:
        logger.warning("No complete months available")
        return
    logger.info(f"Complete months available: {months[0]:%Y-%m} to {months[-1]:%Y-%m}")

    for report_name, dimensions in REPORTS.items():
        report_dir = data_dir / report_name
        report_dir.mkdir(parents=True, exist_ok=True)
        existing_months = {
            date.fromisoformat(f"{path.stem}-01") for path in report_dir.glob("*.jsonl")
        }
        for month in get_months_to_sync(months, existing_months):
            logger.info(f"Fetching {report_name} for {month:%Y-%m}")
            rows = [
                parse_row(row, dimensions)
                for row in fetch_rows(client, site_url, month, dimensions)
            ]
            rows = [row for row in rows if is_significant(row)]
            path = report_dir / f"{month:%Y-%m}.jsonl"
            path.write_text(serialize_rows(rows, dimensions))
            logger.info(f"Saved {len(rows)} rows to {path}")


def fetch_available_dates(client: Any, site_url: str) -> list[date]:
    today = date.today()
    body = {
        "startDate": (today - timedelta(days=LOOKBACK_DAYS)).isoformat(),
        "endDate": today.isoformat(),
        "dimensions": ["date"],
        "rowLimit": ROW_LIMIT,
    }
    response = client.searchanalytics().query(siteUrl=site_url, body=body).execute()
    return [date.fromisoformat(row["keys"][0]) for row in response.get("rows", [])]


def fetch_rows(
    client: Any, site_url: str, month: date, dimensions: list[str]
) -> Iterable[dict[str, Any]]:
    start_row = 0
    while True:
        body = {
            "startDate": month.isoformat(),
            "endDate": get_month_end(month).isoformat(),
            "dimensions": dimensions,
            "rowLimit": ROW_LIMIT,
            "startRow": start_row,
        }
        response = client.searchanalytics().query(siteUrl=site_url, body=body).execute()
        if not (rows := response.get("rows", [])):
            return
        logger.debug(f"Fetched {len(rows)} rows starting at {start_row}")
        yield from rows
        start_row += len(rows)


def pick_site_url(site_urls: list[str]) -> str:
    candidates = sorted(url for url in site_urls if SITE_DOMAIN in url)
    if not candidates:
        raise ValueError(f"No Search Console property for {SITE_DOMAIN}: {site_urls!r}")
    domain_property = f"sc-domain:{SITE_DOMAIN}"
    return domain_property if domain_property in candidates else candidates[0]


def get_complete_months(available_dates: list[date]) -> list[date]:
    """
    Returns first days of months fully covered by the available data,
    so that a month at the edge of the retention period or a month
    which isn't over yet never gets saved incomplete.
    """
    if not available_dates:
        return []
    first_date, last_date = min(available_dates), max(available_dates)
    month = first_date.replace(day=1)
    if month < first_date:
        month = get_next_month(month)
    months = []
    while get_month_end(month) <= last_date:
        months.append(month)
        month = get_next_month(month)
    return months


def get_months_to_sync(months: list[date], existing_months: set[date]) -> list[date]:
    return [month for month in months if month not in existing_months]


def parse_row(row: dict[str, Any], dimensions: list[str]) -> dict[str, Any]:
    keys = dict(zip(dimensions, row["keys"], strict=True))
    if "page" in keys:
        keys["page"] = shorten_url(keys["page"])
    return keys | {
        "clicks": int(row["clicks"]),
        "impressions": int(row["impressions"]),
        "position": round(row["position"], 2),
    }


def shorten_url(url: str) -> str:
    if url.startswith(SITE_ORIGIN):
        return url.removeprefix(SITE_ORIGIN.rstrip("/"))
    return url


def is_significant(row: dict[str, Any]) -> bool:
    return row["clicks"] > 0 or row["impressions"] >= MIN_IMPRESSIONS


def serialize_rows(rows: list[dict[str, Any]], dimensions: list[str]) -> str:
    return "".join(
        f"{json.dumps(row, ensure_ascii=False)}\n"
        for row in sorted(rows, key=itemgetter(*dimensions))
    )


def get_month_end(month: date) -> date:
    return month.replace(day=calendar.monthrange(month.year, month.month)[1])


def get_next_month(month: date) -> date:
    return get_month_end(month) + timedelta(days=1)
