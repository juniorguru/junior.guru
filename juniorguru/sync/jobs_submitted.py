import re
import hashlib
from urllib.parse import urlparse
from datetime import date, timedelta

from juniorguru.lib.md import md
from juniorguru.lib.tasks import sync_task
from juniorguru.lib import google_sheets
from juniorguru.lib.coerce import (coerce, parse_boolean, parse_datetime, parse_text,
    parse_date, parse_set, parse_boolean_words, parse_url)
from juniorguru.models import SubmittedJob, db
from juniorguru.lib import loggers
from juniorguru.sync.scrape_jobs.pipelines.language_parser import parse as parse_language
from juniorguru.sync.jobs_scraped.pipelines.boards_ids import parse_urls as parse_board_ids
from juniorguru.sync.jobs_scraped.pipelines.employment_types_cleaner import clean as clean_employment_types
from juniorguru.lib.locations import fetch_locations


logger = loggers.get(__name__)


DOC_KEY = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'

FIRST_ROW_NO = 2  # skipping sheet header

IMPLICIT_EXPIRATION_DAYS = 30


class DropItem(Exception):
    pass


@sync_task()
@db.connection_context()
def main():
    SubmittedJob.drop_table()
    SubmittedJob.create_table()

    rows = google_sheets.download(google_sheets.get(DOC_KEY, 'jobs'))
    for row_no, row in enumerate(rows, start=FIRST_ROW_NO):
        try:
            job = SubmittedJob.create(**coerce_record(row))
            logger.info(f"Row {row_no} saved as {job!r}")
        except DropItem as e:
            logger.info(f"Row {row_no} dropped. {e}")


def coerce_record(record, today=None):
    data = coerce({
        r'^nadpis pracovní nabídky$': ('title', parse_text),
        r'^timestamp$': ('submitted_at', parse_datetime),
        r'^expire[ds]$': ('expires_on', parse_date),
        r'^approved$': ('approved_on', parse_date),
        r'^email address$': ('apply_email', parse_text),
        r'^externí odkaz na pracovní nabídku$': ('apply_url', parse_url),
        r'^název firmy$': ('company_name', parse_text),
        r'^odkaz na webové stránky firmy$': ('company_url', parse_url),
        r'^město, kde se nachází kancelář$': ('locations_raw', parse_locations),
        r'^je práce na dálku\?$': ('remote', parse_boolean_words),
        r'^pracovní poměr$': ('employment_types', parse_employment_types),
        r'^text pracovní nabídky$': ('description_html', parse_markdown),
        r'\bkup[óo]n\b': ('coupon', parse_boolean),
    }, record)

    if not data.get('approved_on'):
        raise DropItem(f"Not approved: {data['title']!r} submitted on {data['submitted_at']:%Y-%m-%d}")
    data['posted_on'] = data['approved_on']

    if not data.get('expires_on'):
        data['expires_on'] = data['approved_on'] + timedelta(days=IMPLICIT_EXPIRATION_DAYS)

    today = today or date.today()
    if data['expires_on'] <= today:
        raise DropItem(f"Expiration {data['expires_on']:%Y-%m-%d} ≤ today {today:%Y-%m-%d}")

    data['id'] = create_id(data['submitted_at'], data['company_url'])
    data['url'] = f"https://junior.guru/jobs/{data['id']}/"
    urls = filter(None, [data['url'], data.get('apply_url')])
    data['boards_ids'] = parse_board_ids(urls)

    data['lang'] = parse_language(data['description_html'])
    data['locations'] = fetch_locations(data['locations_raw'])
    return data


def parse_locations(value):
    if value:
        return [loc.strip() for loc in re.split(r'\snebo\s', value)]
    return []


def parse_employment_types(value):
    return clean_employment_types(parse_set(value))


def parse_markdown(value):
    if value:
        return md(value.strip())


def create_id(submitted_at, company_url):
    url_parts = urlparse(company_url)
    seed = f'{submitted_at:%Y-%m-%dT%H:%M:%S} {url_parts.netloc}'
    return hashlib.sha224(seed.encode()).hexdigest()
