import subprocess
from multiprocessing import Pool
import hashlib
from urllib.parse import urlparse
from datetime import timedelta

from juniorguru.fetch.lib import timer
from juniorguru.fetch.lib import google_sheets
from juniorguru.fetch.lib.coerce import (coerce, parse_datetime, parse_text,
    parse_date, parse_set)
from juniorguru.models import Job, JobDropped, JobError, db


@timer.notify
def main():
    doc_key = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'
    records = google_sheets.download(google_sheets.get(doc_key, 'jobs'))

    with db:
        for model in [Job, JobError, JobDropped]:
            model.drop_table()
            model.create_table()

        for record in records:
            Job.create(**coerce_record(record))

    Pool().map(run_spider, [
        'linkedin',
        'stackoverflow',
        'startupjobs',
    ])


def coerce_record(record):
    job = coerce({
        r'^timestamp$': ('posted_at', parse_datetime),
        r'^company name$': ('company_name', parse_text),
        r'^employment type$': ('employment_types', parse_set),
        r'^job title$': ('title', parse_text),
        r'^company website link$': ('company_link', parse_text),
        r'^email address$': ('email', parse_text),
        r'^job location$': ('location', parse_text),
        r'^job description$': ('description', parse_text),
        r'^job link$': ('link', parse_text),
        r'^pricing plan$': ('pricing_plan', parse_pricing_plan),
        r'^approved$': ('approved_at', parse_date),
        r'^expire[ds]$': ('expires_at', parse_date),
    }, record)

    if job.get('approved_at') and 'expires_at' not in job:
        job['expires_at'] = job['approved_at'] + timedelta(days=30)
    job['id'] = create_id(job['posted_at'], job['company_link'])
    job['source'] = 'juniorguru'

    return job


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


def run_spider(spider_name):
    return subprocess.run(['scrapy', 'crawl', spider_name], check=True)


if __name__ == '__main__':
    main()
