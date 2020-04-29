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
        'employment_types', 'posted_at', 'description_raw',
    ])
    assert job['title'] == 'My hledáme stále! Přidej se k nám do týmu jako junior linux admin'
    assert job['link'] == 'https://www.startupjobs.cz/nabidka/22025/my-hledame-stale-pridej-se-k-nam-do-tymu-jako-junior-linux-admin?utm_source=juniorguru&utm_medium=cpc&utm_campaign=juniorguru'
    assert job['company_name'] == 'Cloudinfrastack'
    assert job['company_link'] == 'https://www.startupjobs.cz/startup/cloudinfrastack?utm_source=juniorguru&utm_medium=cpc&utm_campaign=juniorguru'
    assert job['location'] == 'Praha, Česko'
    assert job['employment_types'] == ['Part-time', 'Full-time']
    # TODO assert job['posted_at'].date() == date.today() - timedelta(days=27)
    assert '<p>Ahoj, baví tě Linux?' in job['description_raw']


def test_spider_parse_job_types():
    response = XmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'feed-job-types.xml').read_bytes())
    job = next(startupjobs.Spider().parse(response))

    assert job['employment_types'] == ['Full-time', 'External collaboration']


def test_spider_parse_remote():
    response = XmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'feed-remote.xml').read_bytes())
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
