import json
from datetime import date
from pathlib import Path

from lxml import html
from scrapy.http import TextResponse, HtmlResponse

from juniorguru.jobs.legacy_jobs.spiders import remoteok


FIXTURES_DIR = Path(__file__).parent


def normalize_html(html_string):
    return [(el.tag, el.text, el.tail) for el
            in html.fromstring(html_string.strip())]


def test_spider_parse():
    response = TextResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'error.html').read_bytes())
    requests = list(remoteok.Spider().parse(response))

    assert len(requests) == 0


def test_spider_parse_error():
    response = TextResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'api.json').read_bytes())
    requests = list(remoteok.Spider().parse(response))

    assert len(requests) == 7


def test_spider_parse_job():
    json_data = next(filter(lambda jd: jd.get('id') == '99859',
                            json.loads(Path(FIXTURES_DIR / 'api.json').read_bytes())))
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job.html').read_bytes())
    jobs = list(remoteok.Spider().parse_job(response, json_data))

    assert len(jobs) == 1

    job = jobs[0]

    assert sorted(job.keys()) == sorted([
        'title', 'link', 'company_name', 'company_link',
        'posted_at', 'description_html', 'company_logo_urls', 'remote',
    ])
    assert job['title'] == 'Software Engineer II'
    assert job['link'] == 'https://example.com/example/'
    assert job['company_name'] == 'Comscore'
    assert job['company_link'] == 'https://example.com/remote-companies/comscore'
    assert job['remote'] is True
    assert job['posted_at'] == date(2020, 10, 25)
    assert job['company_logo_urls'] == ['https://remoteok.io/assets/jobs/af6ada420dbb093b6fc3cc1dd1a75bb41603782017.png']
    assert (normalize_html(job['description_html']) ==
            normalize_html(Path(FIXTURES_DIR / 'description.html').read_text()))
