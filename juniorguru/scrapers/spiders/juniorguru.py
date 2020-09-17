import hashlib
from urllib.parse import urlparse
from datetime import timedelta

from scrapy import Spider as BaseSpider

from juniorguru.lib import google_sheets
from juniorguru.lib.md import md
from juniorguru.lib.coerce import (coerce, parse_datetime, parse_text,
    parse_date, parse_set)
from juniorguru.scrapers.items import Job
from juniorguru.scrapers.settings import ITEM_PIPELINES


class Spider(BaseSpider):
    name = 'juniorguru'
    custom_settings = {
        'ITEM_PIPELINES': {
            name: priority for name, priority in ITEM_PIPELINES.items()
            if name not in [
                'juniorguru.scrapers.pipelines.short_description_filter.Pipeline',
                'juniorguru.scrapers.pipelines.broken_encoding_filter.Pipeline',
                'juniorguru.scrapers.pipelines.gender_cleaner.Pipeline',
            ]
        }
    }
    doc_key = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'
    sheet_name = 'jobs'

    # https://stackoverflow.com/q/57060667/325365
    # https://developers.google.com/sheets/api/reference/rest#discovery-document
    start_urls = ['https://sheets.googleapis.com/$discovery/rest?version=v4']

    def parse(self, response):
        sheet = google_sheets.get(self.doc_key, self.sheet_name)
        records = google_sheets.download(sheet)

        for record in records:
            yield Job(**coerce_record(record))


def coerce_record(record):
    job = coerce({
        r'^timestamp$': ('posted_at', parse_datetime),
        r'^company name$': ('company_name', parse_text),
        r'^employment type$': ('employment_types', parse_set),
        r'^job title$': ('title', parse_text),
        r'^company website link$': ('company_link', parse_text),
        # r'^email address$': ('email', parse_text),
        r'^job location$': ('location', parse_text),
        r'^job description$': ('description_html', parse_md),
        r'^job link$': ('link', parse_text),
        # r'^pricing plan$': ('pricing_plan', parse_pricing_plan),
        # r'^approved$': ('approved_at', parse_date),
        # r'^expire[ds]$': ('expires_at', parse_date),
    }, record)

    # if job.get('approved_at') and 'expires_at' not in job:
    #     job['expires_at'] = job['approved_at'] + timedelta(days=30)
    # job['id'] = create_id(job['posted_at'], job['company_link'])

    return job


def parse_md(markdown_text):
    return md(parse_text(markdown_text))


def parse_pricing_plan(value):
    if value:
        value = value.strip().lower()
        if 'flat rate' in value:
            return 'annual_flat_rate'
        if not value.startswith('0 czk'):
            return 'standard'
    return 'community'


def create_id(posted_at, company_link):
    url_parts = urlparse(company_link)
    seed = f'{posted_at:%Y-%m-%dT%H:%M:%S} {url_parts.netloc}'
    return hashlib.sha224(seed.encode()).hexdigest()
