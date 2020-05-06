from datetime import date, timedelta
from pathlib import Path

import pytest
from scrapy.http import HtmlResponse

from juniorguru.scrapers.spiders import linkedin


FIXTURES_DIR = Path(__file__).parent


def test_spider_parse():
    response = HtmlResponse('https://example.com/seeMoreJobPostings/',
                            body=Path(FIXTURES_DIR / 'more.html').read_bytes())
    requests = list(linkedin.Spider().parse(response))
    job_requests = list(filter(lambda r: '/jobs/view/' in r.url, requests))
    more_requests = list(filter(lambda r: '/seeMoreJobPostings/' in r.url, requests))

    assert len(job_requests) == 25
    assert 'position' not in job_requests[0].url
    assert 'pageNum' not in job_requests[0].url

    assert len(more_requests) == 1
    assert 'start=25' in more_requests[0].url


def test_spider_parse_end():
    response = HtmlResponse('https://example.com/seeMoreJobPostings/',
                            body=Path(FIXTURES_DIR / 'more_end.html').read_bytes())
    requests = list(linkedin.Spider().parse(response))
    job_requests = list(filter(lambda r: '/jobs/view/' in r.url, requests))
    more_requests = list(filter(lambda r: '/seeMoreJobPostings/' in r.url, requests))

    assert len(job_requests) == 21
    assert len(more_requests) == 0


def test_spider_parse_job():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job.html').read_bytes())
    jobs = list(linkedin.Spider().parse_job(response))

    assert len(jobs) == 1

    job = jobs[0]

    assert sorted(job.keys()) == sorted([
        'title', 'link', 'company_name', 'company_link', 'location',
        'employment_types', 'posted_at', 'description_raw',
        'experience_levels',
    ])
    assert job['title'] == 'Start kariéry jako Junior C++ Programátor/ka'
    assert job['link'] == 'https://example.com/example/'
    assert job['company_name'] == 'Experis Czech Republic'
    assert job['company_link'] == 'https://cz.linkedin.com/company/experis-czech-republic?trk=public_jobs_topcard_org_name'
    assert job['location'] == 'Prague, Czech Republic'
    assert job['employment_types'] == ['full-time']
    assert job['experience_levels'] == ['entry level']
    assert job['posted_at'].date() == date.today() - timedelta(weeks=3)
    assert '<li>3 Sick days ročně' in job['description_raw']


def test_spider_parse_job_description_doesnt_include_criteria_list():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job.html').read_bytes())
    job = next(linkedin.Spider().parse_job(response))

    assert 'Employment type' not in job['description_raw']
    assert 'Information Technology and Services' not in job['description_raw']


def test_spider_parse_job_no_company_link():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job_no_company_link.html').read_bytes())
    job = next(linkedin.Spider().parse_job(response))

    assert job['company_name'] == 'Ubiquiti'
    assert 'company_link' not in job
    assert job['location'] == 'Pilsen, Plzeň, Czech Republic'


def test_spider_parse_job_applicants():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job_applicants.html').read_bytes())
    job = next(linkedin.Spider().parse_job(response))

    assert job['posted_at'].date() == date.today() - timedelta(weeks=2)


@pytest.mark.parametrize('url,param_names,expected', [
    ('https://example.com', ['a', 'b'], 'https://example.com'),
    ('https://example.com?a=1&b=2', ['a', 'b'], 'https://example.com'),
    ('https://example.com?a=1&c=3&b=2', ['a', 'b'], 'https://example.com?c=3'),
    ('https://example.com', [], 'https://example.com'),
    ('https://example.com?a=1&b=2', [], 'https://example.com?a=1&b=2'),
])
def test_strip_params(url, param_names, expected):
    assert linkedin.strip_params(url, param_names) == expected


@pytest.mark.parametrize('url,param_name,expected', [
    ('https://example.com', 'b', 'https://example.com?b=1'),
    ('https://example.com?a=1&b=2&c=3', 'b', 'https://example.com?a=1&b=3&c=3'),
])
def test_increment_param(url, param_name, expected):
    assert linkedin.increment_param(url, param_name) == expected


@pytest.mark.parametrize('url,param_name,inc,expected', [
    ('https://example.com', 'b', 25, 'https://example.com?b=25'),
    ('https://example.com?a=1&b=2&c=3', 'b', 25, 'https://example.com?a=1&b=27&c=3'),
])
def test_increment_param_inc(url, param_name, inc, expected):
    assert linkedin.increment_param(url, param_name, inc) == expected
