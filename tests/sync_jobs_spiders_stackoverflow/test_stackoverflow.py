from datetime import date, timedelta
from pathlib import Path

from scrapy.http import HtmlResponse

from juniorguru.jobs.legacy_jobs.spiders import stackoverflow


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

    assert sorted(job.keys()) == sorted([
        'title', 'link', 'company_name', 'company_link', 'locations_raw',
        'employment_types', 'posted_at', 'description_html',
        'experience_levels', 'company_logo_urls', 'remote',
    ])
    assert job['title'] == 'Solution Engineer (M/F/X)'
    assert job['link'] == 'https://example.com/example/'
    assert job['company_name'] == 'QUAJOO GmbH'
    assert job['company_link'] == 'https://example.com/jobs/companies/quajoo-gmbh'
    assert job['locations_raw'] == ['Leipzig, Deutschland']
    assert job['employment_types'] == ['Full-time']
    assert job['experience_levels'] == ['junior', 'mid-level']
    assert job['posted_at'] == date.today() - timedelta(days=27)
    assert job['company_logo_urls'] == ['https://i.stack.imgur.com/kUWEv.png']
    assert 'what QUAJOO offers you:</strong>' in job['description_html']


def test_spider_parse_job_via():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job_via.html').read_bytes())
    job = next(stackoverflow.Spider().parse_job(response))

    assert job['company_name'] == 'CBOE Global Markets'
    assert job['company_link'] == 'https://www.cboe.com/'
    assert job['locations_raw'] == ['London, UK']


def test_spider_parse_job_remote():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job_remote.html').read_bytes())
    job = next(stackoverflow.Spider().parse_job(response))

    assert job['company_name'] == 'Hummingbot'
    assert job['company_link'] == 'https://example.com/jobs/companies/hummingbot'
    assert job['remote'] is True
    assert job.get('locations_raw') is None


def test_spider_parse_job_posted_at_as_li():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job_posted_at_as_li.html').read_bytes())
    job = next(stackoverflow.Spider().parse_job(response))

    assert job['posted_at'] == date.today() - timedelta(days=29)


def test_clean_location():
    assert stackoverflow.clean_location('''
        \r\n                    –\r\nLeipzig, Deutschland
    ''') == 'Leipzig, Deutschland'


def test_clean_location_remote():
    assert stackoverflow.clean_location('No office location') is None
