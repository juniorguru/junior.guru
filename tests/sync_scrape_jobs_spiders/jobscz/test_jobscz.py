from datetime import date
from pathlib import Path

import pytest
from scrapy.http import HtmlResponse

from juniorguru.sync.scrape_jobs.spiders import jobscz


FIXTURES_DIR = Path(__file__).parent


def test_spider_parse():
    listing_url = 'https://beta.www.jobs.cz/prace/?field%5B%5D=200900013&field%5B%5D=200900012&suitable-for=graduates&cacheKey=ae78dde7-1eee-4e59-936f-13ed3541890c'
    response = HtmlResponse(listing_url,
                            body=Path(FIXTURES_DIR / 'listing.html').read_bytes())
    requests = list(jobscz.Spider().parse(response))

    assert len(requests) == 37

    assert requests[0].url == 'https://beta.www.jobs.cz/rpd/1615173381/?searchId=9d26cd7f-d018-4340-ab3f-f6f1719ce5a9&rps=228'
    item = requests[0].cb_kwargs['item']
    assert item['source'] == 'jobscz'
    assert item['first_seen_on'] == date.today()
    assert item['title'] == 'Systémový administrátor/administrátorka senior'
    assert item['company_name'] == 'Fio banka, a.s.'
    assert item['locations_raw'] == ['Praha – Nové Město']
    assert item['company_logo_urls'] == ['https://my.teamio.com/recruit/logo?id=66c81923-c5e2-4969-868b-069c1b63f6e9&v=1587555697131']
    assert item['source_urls'] == [listing_url]

    assert requests[1].url == 'https://beta.www.jobs.cz/rpd/1613133866/?searchId=9d26cd7f-d018-4340-ab3f-f6f1719ce5a9&rps=228'
    item = requests[1].cb_kwargs['item']
    assert item['source'] == 'jobscz'
    assert item['first_seen_on'] == date.today()
    assert item['title'] == 'Aplikační specialista pro eBay'
    assert item['company_name'] == 'MoroSystems, s.r.o.'
    assert item['locations_raw'] == ['Praha – Karlín']
    assert 'company_logo_urls' not in item
    assert item['source_urls'] == [listing_url]


@pytest.mark.skip('work in progress')
def test_spider_parse_job_custom():
    response = HtmlResponse('https://fio.jobs.cz/detail-pozice?r=detail&id=1615173381&rps=228&impressionId=ac8f8a52-70fe-4be5-b32e-9f6e6b1c2b23',
                            body=Path(FIXTURES_DIR / 'job_custom.html').read_bytes())

    jobs = list(jobscz.Spider().parse_job(response, 'https://beta.www.jobs.cz/prace/...'))
    assert len(jobs) == 0


@pytest.mark.skip('work in progress')
def test_spider_parse_job():
    response = HtmlResponse('https://beta.www.jobs.cz/rpd/1613133866/?searchId=ac8f8a52-70fe-4be5-b32e-9f6e6b1c2b23&rps=228',
                            body=Path(FIXTURES_DIR / 'job.html').read_bytes())

    jobs = list(jobscz.Spider().parse_job(response, 'https://beta.www.jobs.cz/prace/...'))
    assert len(jobs) == 1

    job = jobs[0]

    assert sorted(job.keys()) == sorted([
        'title', 'url', 'company_name', 'locations_raw',
        'employment_types', 'first_seen_on', 'description_html',
        'source', 'source_urls',
    ])
    assert job['title'] == 'Network Reliability Engineer'
    assert job['url'] == 'https://beta.www.jobs.cz/rpd/1613133866/'
    assert job['company_name'] == 'ComSource s.r.o.'
    assert job['locations_raw'] == ['Nad Vršovskou horou 1423/10, Praha – Michle']
    assert job['employment_types'] == ['Práce na plný úvazek']
    assert job['first_seen_on'] == date.today()
    assert job['source'] == 'jobscz'
    assert job['source_urls'] == ['https://beta.www.jobs.cz/prace/...',
                                  'https://beta.www.jobs.cz/rpd/1613133866/?searchId=ac8f8a52-70fe-4be5-b32e-9f6e6b1c2b23&rps=228']
    assert '<p class="typography-body-large-text-regular mb-900">ComSource s r.o.\nSpolečnost Comsource s.r.o. je dynamicky se rozvíjející' in job['description_html']
    assert 'ComSource</strong>' in job['description_html']


@pytest.mark.skip('work in progress')
def test_spider_parse_job_company_en():
    response = HtmlResponse('https://beta.www.jobs.cz/fp/fortuna-game-a-s-5118444/1614397443/',
                            body=Path(FIXTURES_DIR / 'job_company_en.html').read_bytes())
    job = next(jobscz.Spider().parse_job(response, 'https://beta.www.jobs.cz/prace/...'))

    assert job['company_name'] == 'FORTUNA GAME a.s.'
    assert job['company_url'] == 'https://beta.www.jobs.cz/fp/fortuna-game-a-s-5118444/'
    assert job['locations_raw'] == ['Italská 2584/69, Praha – Vinohrady']
    assert job['employment_types'] == ['Full-time work']
    assert job['company_logo_urls'] == ['https://aeqqktywno.cloudimg.io/bound/200x100/n/_cpimg_prod_/5118444/1f8fd1ae-6e76-11ea-99e6-0242ac110010.png']
    assert '<h2>Group Release &amp; Defect Manager</h2>' in job['description_html']
