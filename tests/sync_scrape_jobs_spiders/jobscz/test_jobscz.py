from pathlib import Path

from scrapy.http import HtmlResponse

from juniorguru.sync.scrape_jobs.spiders import jobscz


FIXTURES_DIR = Path(__file__).parent


def test_spider_parse():
    response = HtmlResponse('https://beta.www.jobs.cz/prace/?field%5B%5D=200900013&field%5B%5D=200900012&suitable-for=graduates&cacheKey=ae78dde7-1eee-4e59-936f-13ed3541890c',
                            body=Path(FIXTURES_DIR / 'search.html').read_bytes())
    requests = list(jobscz.Spider().parse(response))

    assert len(requests) == 37
    assert requests[0].url == 'https://beta.www.jobs.cz/rpd/1615173381/?searchId=9d26cd7f-d018-4340-ab3f-f6f1719ce5a9&rps=228'


def test_spider_parse_job_custom():
    response = HtmlResponse('https://fio.jobs.cz/detail-pozice?r=detail&id=1615173381&rps=228&impressionId=ac8f8a52-70fe-4be5-b32e-9f6e6b1c2b23',
                            body=Path(FIXTURES_DIR / 'job_custom.html').read_bytes())

    jobs = list(jobscz.Spider().parse_job(response, 'https://beta.www.jobs.cz/prace/...'))
    assert len(jobs) == 0


def test_spider_parse_job():
    response = HtmlResponse('https://beta.www.jobs.cz/rpd/1613133866/?searchId=ac8f8a52-70fe-4be5-b32e-9f6e6b1c2b23&rps=228',
                            body=Path(FIXTURES_DIR / 'job.html').read_bytes())

    jobs = list(jobscz.Spider().parse_job(response, 'https://beta.www.jobs.cz/prace/...'))
    assert len(jobs) == 1

    job = jobs[0]

    # assert sorted(job.keys()) == sorted([
    #     'title', 'url', 'company_name', 'locations_raw',
    #     'employment_types', 'first_seen_on', 'description_html',
    #     'experience_levels', 'company_logo_urls', 'remote',
    #     'source', 'source_urls',
    # ])
    assert job['title'] == 'Network Reliability Engineer'
    assert job['url'] == 'https://beta.www.jobs.cz/rpd/1613133866/'
    # assert job['company_name'] == 'Komerční banka'
    # assert job['locations_raw'] == ['Prague, Czechia']
    # assert job['remote'] is False
    # assert job['employment_types'] == ['full-time']
    # assert job['experience_levels'] == ['entry level']
    # assert job['first_seen_on'] == date.today() - timedelta(weeks=1)
    # assert job['company_logo_urls'] == ['https://media-exp1.licdn.com/dms/image/C560BAQHxuVQO-Rz9rw/company-logo_100_100/0/1546508771908?e=1640217600&v=beta&t=hUZKjJ2dnPP92AcBOKAEFzFqEdD-OB9WwS0X18LoyP4']
    # assert job['source'] == 'linkedin'
    # assert job['source_urls'] == ['https://example.com/search?foo=1', 'https://example.com/example/']
    assert '<p class="typography-body-large-text-regular mb-900">ComSource s r.o.\nSpolečnost Comsource s.r.o. je dynamicky se rozvíjející' in job['description_html']
    assert 'ComSource</strong>' in job['description_html']
