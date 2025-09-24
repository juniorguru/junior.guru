import hashlib
import re
from datetime import date, timedelta
from urllib.parse import urlparse

from jg.coop.cli.sync import main as cli
from jg.coop.lib import google_sheets, loggers
from jg.coop.lib.google_coerce import (
    coerce,
    parse_boolean,
    parse_boolean_words,
    parse_date,
    parse_datetime,
    parse_set,
    parse_text,
    parse_url,
)
from jg.coop.lib.lang import parse_language
from jg.coop.lib.md import md
from jg.coop.lib.text import extract_text
from jg.coop.models.base import db
from jg.coop.models.job import SubmittedJob
from jg.coop.sync.jobs_scraped.pipelines.boards_ids import (
    parse_urls as parse_board_ids,
)
from jg.coop.sync.jobs_scraped.pipelines.employment_types_cleaner import (
    clean_employment_types,
)


logger = loggers.from_path(__file__)


DOC_KEY = "1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls"

FIRST_ROW_NO = 2  # skipping sheet header

IMPLICIT_EXPIRATION_DAYS = 30


class DropItem(Exception):
    pass


@cli.sync_command()
@db.connection_context()
def main():
    SubmittedJob.drop_table()
    SubmittedJob.create_table()

    rows = google_sheets.download(google_sheets.get(DOC_KEY, "jobs"))
    for row_no, row in enumerate(rows, start=FIRST_ROW_NO):
        try:
            job = SubmittedJob.create(**coerce_record(row))
            logger.info(f"Row {row_no} saved as {job!r}")
        except DropItem as e:
            logger.info(f"Row {row_no} dropped. {e}")


def coerce_record(record, today=None):
    data = coerce(
        {
            r"^nadpis pracovní nabídky$": ("title", parse_text),
            r"^timestamp$": ("submitted_at", parse_datetime),
            r"^expire[ds]$": ("expires_on", parse_date),
            r"^approved$": ("approved_on", parse_date),
            r"^email address$": ("apply_email", parse_text),
            r"^externí odkaz na pracovní nabídku$": ("apply_url", parse_url),
            r"^název firmy$": ("company_name", parse_text),
            r"^odkaz na webové stránky firmy$": ("company_url", parse_url),
            r"^město, kde se nachází kancelář$": ("locations_raw", parse_locations),
            r"^je práce na dálku\?$": ("remote", parse_boolean_words),
            r"^pracovní poměr$": ("employment_types", parse_employment_types),
            r"^text pracovní nabídky$": ("description_html", parse_markdown),
            r"\bkup[óo]n\b": ("coupon", parse_boolean),
        },
        record,
    )

    if not data.get("approved_on"):
        raise DropItem(
            f"Not approved: {data['title']!r} submitted on {data['submitted_at']:%Y-%m-%d}"
        )
    data["posted_on"] = data["approved_on"]

    if not data.get("expires_on"):
        data["expires_on"] = data["approved_on"] + timedelta(
            days=IMPLICIT_EXPIRATION_DAYS
        )

    today = today or date.today()
    if data["expires_on"] <= today:
        raise DropItem(
            f"Expiration {data['expires_on']:%Y-%m-%d} ≤ today {today:%Y-%m-%d}"
        )

    data["id"] = create_id(data["submitted_at"], data["company_url"])
    data["url"] = f"https://junior.guru/jobs/{data['id']}/"
    urls = filter(None, [data["url"], data.get("apply_url")])
    data["boards_ids"] = parse_board_ids(urls)

    data["description_text"] = extract_text(data["description_html"])
    data["lang"] = parse_language(data["description_text"])
    return data


def parse_locations(value):
    if value:
        return [loc.strip() for loc in re.split(r"\snebo\s", value)]
    return []


def parse_employment_types(value):
    return clean_employment_types(parse_set(value))


def parse_markdown(value):
    if value:
        return md(value.strip())


def create_id(submitted_at, company_url):
    url_parts = urlparse(company_url)
    seed = f"{submitted_at:%Y-%m-%dT%H:%M:%S} {url_parts.netloc}"
    return hashlib.sha224(seed.encode()).hexdigest()
