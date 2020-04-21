from pathlib import Path
from datetime import date, datetime, timedelta

import pytest
from scrapy.http import HtmlResponse

from juniorguru.scrapers.spiders import stackoverflow


FIXTURES_DIR = Path(__file__).parent


def test_spider_parse():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'jobs.html').read_bytes())
    requests = list(stackoverflow.Spider().parse(response))
    job_requests = list(filter(lambda r: '/jobs/' in r.url, requests))
    pagination_requests = list(filter(lambda r: '/jobs?' in r.url, requests))

    assert len(job_requests) == 25
    assert len(pagination_requests) == 7


def test_spider_parse_job():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job.html').read_bytes())
    jobs = list(stackoverflow.Spider().parse_job(response))

    assert len(jobs) == 1

    job = jobs[0]

    assert list(job.keys()) == [
        'title', 'link', 'company_name', 'company_link', 'location_raw',
        'employment_types', 'posted_at', 'description_raw'
    ]
    assert job['title'] == 'Solution Engineer (M/F/X)'
    assert job['link'] == 'https://example.com/example/'
    assert job['company_name'] == 'QUAJOO GmbH'
    assert job['company_link'] == 'https://example.com/jobs/companies/quajoo-gmbh'
    assert job['location_raw'] == 'Leipzig, Deutschland'
    assert job['employment_types'] == ['Full-time']
    assert job['posted_at'].date() == date.today() - timedelta(days=27)
    assert 'what QUAJOO offers you:</strong>' in job['description_raw']


def test_clean_location_raw():
    assert stackoverflow.clean_location_raw('''
        \r\n                    –\r\nLeipzig, Deutschland
    ''') == 'Leipzig, Deutschland'


@pytest.mark.parametrize('time,expected', [
    (' Posted 13 days ago', date(2020, 4, 7)),
    (' Posted 4 hours ago', date(2020, 4, 20)),
    (' Posted < 1 hour ago', date(2020, 4, 20)),
    (' Posted yesterday', date(2020, 4, 19)),
])
def test_parse_relative_time(time, expected):
    now = datetime(2020, 4, 20, 20, 1, 45)
    assert stackoverflow.parse_relative_time(time, now=now).date() == expected


def test_parse_relative_time_raises_on_uncrecognized_value():
    with pytest.raises(ValueError):
        stackoverflow.parse_relative_time('gargamel')
