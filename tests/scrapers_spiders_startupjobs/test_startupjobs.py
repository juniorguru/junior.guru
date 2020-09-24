from datetime import date
from pathlib import Path

import pytest
from scrapy.http import XmlResponse

from juniorguru.scrapers.spiders import startupjobs


FIXTURES_DIR = Path(__file__).parent


def test_spider_parse():
    response = XmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'feed.xml').read_bytes())
    jobs = list(startupjobs.Spider().parse(response))

    assert len(jobs) == 2

    job = jobs[0]

    assert sorted(job.keys()) == sorted([
        'title', 'link', 'company_name', 'company_link', 'location',
        'employment_types', 'posted_at', 'description_html', 'company_logo_urls',
    ])
    assert job['title'] == 'My hledáme stále! Přidej se k nám do týmu jako junior linux admin'
    assert job['link'] == 'https://www.startupjobs.cz/nabidka/22025/my-hledame-stale-pridej-se-k-nam-do-tymu-jako-junior-linux-admin?utm_source=juniorguru&utm_medium=cpc&utm_campaign=juniorguru'
    assert job['company_name'] == 'Cloudinfrastack'
    assert job['company_link'] == 'https://www.startupjobs.cz/startup/cloudinfrastack?utm_source=juniorguru&utm_medium=cpc&utm_campaign=juniorguru'
    assert job['location'] == 'Praha, Česko'
    assert job['employment_types'] == ['Part-time', 'Full-time']
    assert job['posted_at'] == date(2020, 5, 5)
    assert job['company_logo_urls'] == ['https://www.startupjobs.cz/uploads/U56OHNIPVP54cloudinfrastack-fb-logo-180x180-1154411059762.png']
    assert '<p>Ahoj, baví tě Linux?' in job['description_html']


def test_spider_parse_job_types():
    response = XmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'feed_job_types.xml').read_bytes())
    job = next(startupjobs.Spider().parse(response))

    assert job['employment_types'] == ['Full-time', 'External collaboration']


def test_spider_parse_html_entities():
    response = XmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'feed_html_entities.xml').read_bytes())
    job = next(startupjobs.Spider().parse(response))

    assert job['title'] == 'Analytik&programátor Junior'
    assert job['company_name'] == 'P&J Capital'


def test_spider_parse_cities():
    response = XmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'feed_cities.xml').read_bytes())
    jobs = list(startupjobs.Spider().parse(response))

    assert len(jobs) == 2

    assert jobs[0]['location'] == 'Praha, Česko'
    assert jobs[1]['location'] == 'Olomouc, Česko'
    assert jobs[0]['link'] == jobs[1]['link']

    jobs[0]['title'] = 'Modified'  # testing whether the job objects are copies

    assert jobs[1]['title'] == 'Server / Cloud / DevOps Admin'


def test_spider_parse_cities_job_objects_are_copies():
    response = XmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'feed_cities.xml').read_bytes())
    jobs = list(startupjobs.Spider().parse(response))
    jobs[0]['title'] = 'Modified'

    assert jobs[0]['link'] == jobs[1]['link']
    assert jobs[0]['title'] == 'Modified'
    assert jobs[1]['title'] == 'Server / Cloud / DevOps Admin'


def test_spider_parse_remote():
    response = XmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'feed_remote.xml').read_bytes())
    job = next(startupjobs.Spider().parse(response))

    assert job['employment_types'] == ['Part-time', 'External collaboration']


@pytest.mark.parametrize('types,expected', [
    ([], []),
    (['full-time', 'remote', 'part-time'], ['full-time', 'part-time']),
    (['remote', 'remote'], []),
    (['full-time', 'part-time'], ['full-time', 'part-time']),
])
def test_drop_remote(types, expected):
    startupjobs.drop_remote(types) == expected


@pytest.mark.parametrize('value,expected', [
    ('2020-05-07T16:06:08+02:00', date(2020, 5, 7)),
    ('2020-05-07T16:06:08-02:00', date(2020, 5, 7)),
    ('2020-05-07T16:06:08', date(2020, 5, 7)),
    ('2020-05-07 16:06:08', date(2020, 5, 7)),
])
def test_parse_iso_date(value, expected):
    assert startupjobs.parse_iso_date(value) == expected
