from datetime import date
from pathlib import Path

from scrapy.http import HtmlResponse

from juniorguru.sync.scrape_jobs.items import Job
from juniorguru.sync.scrape_jobs.spiders import jobscz


FIXTURES_DIR = Path(__file__).parent


def test_spider_parse():
    response = HtmlResponse('https://beta.www.jobs.cz/prace/...',
                            body=Path(FIXTURES_DIR / 'listing.html').read_bytes())
    requests = list(jobscz.Spider().parse(response))

    assert len(requests) == 37 + 4  # jobs + pagination (without page=1)

    assert requests[0].url == 'https://beta.www.jobs.cz/rpd/1615173381/?searchId=9d26cd7f-d018-4340-ab3f-f6f1719ce5a9&rps=228'
    item = requests[0].cb_kwargs['item']
    assert sorted(item.keys()) == sorted([
        'title', 'company_name', 'locations_raw',
        'first_seen_on', 'company_logo_urls', 'source', 'source_urls',
    ])
    assert item['source'] == 'jobscz'
    assert item['first_seen_on'] == date.today()
    assert item['title'] == 'Systémový administrátor/administrátorka senior'
    assert item['company_name'] == 'Fio banka, a.s.'
    assert item['locations_raw'] == ['Praha – Nové Město']
    assert item['company_logo_urls'] == ['https://my.teamio.com/recruit/logo?id=66c81923-c5e2-4969-868b-069c1b63f6e9&v=1587555697131']
    assert item['source_urls'] == ['https://beta.www.jobs.cz/prace/...', 'https://beta.www.jobs.cz/rpd/1615173381/?searchId=9d26cd7f-d018-4340-ab3f-f6f1719ce5a9&rps=228']

    assert requests[37].url == 'https://beta.www.jobs.cz/prace/?field%5B0%5D=200900013&field%5B1%5D=200900012&suitable-for=graduates&cacheKey=ae78dde7-1eee-4e59-936f-13ed3541890c&page=2'
    assert requests[-1].url == 'https://beta.www.jobs.cz/prace/?field%5B0%5D=200900013&field%5B1%5D=200900012&suitable-for=graduates&cacheKey=ae78dde7-1eee-4e59-936f-13ed3541890c&page=5'


def test_spider_parse_without_logo():
    response = HtmlResponse('https://beta.www.jobs.cz/prace/...',
                            body=Path(FIXTURES_DIR / 'listing.html').read_bytes())
    requests = list(jobscz.Spider().parse(response))

    assert requests[1].url == 'https://beta.www.jobs.cz/rpd/1613133866/?searchId=9d26cd7f-d018-4340-ab3f-f6f1719ce5a9&rps=228'
    assert 'company_logo_urls' not in requests[1].cb_kwargs['item']


def test_spider_parse_job_custom():
    response = HtmlResponse('https://fio.jobs.cz/detail-pozice?r=detail&id=1615173381&rps=228&impressionId=ac8f8a52-70fe-4be5-b32e-9f6e6b1c2b23',
                            body=Path(FIXTURES_DIR / 'job_custom.html').read_bytes())
    jobs = list(jobscz.Spider().parse_job(response, Job()))

    assert len(jobs) == 0


def test_spider_parse_job_standard():
    response = HtmlResponse('https://beta.www.jobs.cz/rpd/1613133866/?searchId=ac8f8a52-70fe-4be5-b32e-9f6e6b1c2b23&rps=228',
                            body=Path(FIXTURES_DIR / 'job_standard.html').read_bytes())
    job = next(jobscz.Spider().parse_job(response, Job()))

    assert sorted(job.keys()) == sorted(['employment_types', 'description_html', 'source_urls', 'url'])
    assert job['url'] == 'https://beta.www.jobs.cz/rpd/1613133866/'
    assert job['employment_types'] == ['práce na plný úvazek']
    assert job['source_urls'] == ['https://beta.www.jobs.cz/rpd/1613133866/?searchId=ac8f8a52-70fe-4be5-b32e-9f6e6b1c2b23&rps=228']

    assert '>Úvodní představení</p>' not in job['description_html']
    assert '<p class="typography-body-large-text-regular mb-900">ComSource s r.o.\nSpolečnost Comsource s.r.o. je dynamicky se rozvíjející' in job['description_html']

    assert '>Pracovní nabídka</p>' not in job['description_html']
    assert '<strong>Požadavky:</strong>' in job['description_html']


def test_spider_parse_job_standard_en():
    response = HtmlResponse('https://beta.www.jobs.cz/rpd/1613133866/',
                            body=Path(FIXTURES_DIR / 'job_standard_en.html').read_bytes())
    job = next(jobscz.Spider().parse_job(response, Job()))

    assert sorted(job.keys()) == sorted(['employment_types', 'description_html', 'source_urls', 'url'])
    assert job['employment_types'] == ['full-time work', 'part-time work']

    assert '>Úvodní představení</p>' not in job['description_html']
    assert 'bezpilotních letounů UAV i antidronové' in job['description_html']

    assert '>Pracovní nabídka</p>' not in job['description_html']
    assert '<strong>Areas of Our Projects</strong>' in job['description_html']


def test_spider_parse_job_company():
    response = HtmlResponse('https://beta.www.jobs.cz/fp/onsemi-61382/1597818748/?positionOfAdInAgentEmail=0&searchId=ac8f8a52-70fe-4be5-b32e-9f6e6b1c2b23&rps=233',
                            body=Path(FIXTURES_DIR / 'job_company.html').read_bytes())
    job = next(jobscz.Spider().parse_job(response, Job()))

    assert sorted(job.keys()) == sorted(['employment_types', 'description_html', 'source_urls', 'url', 'company_url'])
    assert job['url'] == 'https://beta.www.jobs.cz/fp/onsemi-61382/1597818748/'
    assert job['employment_types'] == ['práce na plný úvazek']
    assert job['source_urls'] == ['https://beta.www.jobs.cz/fp/onsemi-61382/1597818748/?positionOfAdInAgentEmail=0&searchId=ac8f8a52-70fe-4be5-b32e-9f6e6b1c2b23&rps=233']
    assert job['company_url'] == 'https://beta.www.jobs.cz/fp/onsemi-61382/'

    assert 'Světoví producenti elektroniky či aut s námi spolupracují a čekají na naše inovativní čipy' in job['description_html']
    assert '<h2>Vývojář polovodičových součástek a automatizace v TCAD</h2>' not in job['description_html']
    assert 'Zkušenost s deskami z karbidu křemíku' in job['description_html']


def test_spider_parse_job_company_en():
    response = HtmlResponse('https://beta.www.jobs.cz/fp/onsemi-61382/1597818748/',
                            body=Path(FIXTURES_DIR / 'job_company_en.html').read_bytes())
    job = next(jobscz.Spider().parse_job(response, Job()))

    assert sorted(job.keys()) == sorted(['employment_types', 'description_html', 'source_urls', 'url', 'company_url'])
    assert job['employment_types'] == ['full-time work']

    assert 'Our new home is the remarkable Churchill II building' in job['description_html']
    assert '<h2>Group Release &amp; Defect Manager</h2>' not in job['description_html']
    assert '<strong>RESPONSIBILITIES:</strong>' in job['description_html']
