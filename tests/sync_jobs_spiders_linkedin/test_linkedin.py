from datetime import date, timedelta
from pathlib import Path

import pytest
from scrapy.http import HtmlResponse

from juniorguru.sync.jobs.spiders import linkedin


FIXTURES_DIR = Path(__file__).parent


def test_spider_parse():
    response = HtmlResponse('https://example.com/seeMoreJobPostings/',
                            body=Path(FIXTURES_DIR / 'more.html').read_bytes())
    requests = list(linkedin.Spider().parse(response))
    job_requests = list(filter(lambda r: '/jobPosting/' in r.url, requests))
    more_requests = list(filter(lambda r: '/seeMoreJobPostings/' in r.url, requests))

    assert len(job_requests) == 25
    assert job_requests[0].url == 'https://cz.linkedin.com/jobs-guest/jobs/api/jobPosting/1846698040'

    assert len(more_requests) == 1
    assert 'start=25' in more_requests[0].url


def test_spider_parse_end():
    response = HtmlResponse('https://example.com/seeMoreJobPostings/',
                            body=Path(FIXTURES_DIR / 'more_end.html').read_bytes())
    requests = list(linkedin.Spider().parse(response))
    job_requests = list(filter(lambda r: '/jobPosting/' in r.url, requests))
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
        'title', 'link', 'company_name', 'company_link', 'locations_raw',
        'employment_types', 'posted_at', 'description_html',
        'experience_levels', 'company_logo_urls', 'remote',
    ])
    assert job['title'] == 'Software Engineer'
    assert job['link'] == 'https://ca.linkedin.com/jobs/view/software-engineer-at-adaptavist-2230926500'
    assert job['company_name'] == 'Adaptavist'
    assert job['company_link'] == 'https://uk.linkedin.com/company/adaptavist'
    assert job['locations_raw'] == ['Toronto, Ontario, Canada']
    assert job['remote'] is False
    assert job['employment_types'] == ['full-time']
    assert job['experience_levels'] == ['entry level']
    assert job['posted_at'] == date.today() - timedelta(weeks=3)
    assert job['company_logo_urls'] == ['https://media-exp1.licdn.com/dms/image/C4D0BAQHhfg0SSuymNA/company-logo_100_100/0?e=1612396800&v=beta&t=GoeZ9Wui3hJSaLrewZdVNpWFm3YCMOSsmte2maE7S3o']
    assert '<li>ReactJS, Webpack</li>' in job['description_html']


def test_spider_parse_job_september_2021():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job_september_2021.html').read_bytes())
    jobs = list(linkedin.Spider().parse_job(response))

    assert len(jobs) == 1

    job = jobs[0]

    # assert sorted(job.keys()) == sorted([
    #     'title', 'link', 'company_name', 'company_link', 'locations_raw',
    #     'employment_types', 'posted_at', 'description_html',
    #     'experience_levels', 'company_logo_urls', 'remote',
    # ])
    assert job['title'] == '.NET Junior Developer'
    assert job['link'] == 'https://cz.linkedin.com/jobs/view/net-junior-developer-at-roivenue%E2%84%A2-2665331232'
    assert job['company_name'] == 'ROIVENUE™'
    assert job['company_link'] == 'https://cz.linkedin.com/company/roivenue'
    assert job['locations_raw'] == ['Hlavní město Praha, Česko']
    assert job['remote'] is False
    assert job['employment_types'] == ['full-time']
    assert job['experience_levels'] == ['entry level']
    assert job['posted_at'] == date.today() - timedelta(days=3)
    assert job['company_logo_urls'] == ['https://media-exp1.licdn.com/dms/image/C4D0BAQE5dJwgWcSH0g/company-logo_100_100/0/1545137392551?e=1639612800&v=beta&t=q8nYHCU6u2RqmYfqKT0l-BZfC5NgKoNnztsvI1W-gYU']
    assert '<li>.NET at least at level 3/5</li>' in job['description_html']


@pytest.mark.skip('missing a test fixture')
def test_spider_parse_job_description_doesnt_include_criteria_list():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job.html').read_bytes())
    job = next(linkedin.Spider().parse_job(response)).cb_kwargs['item']

    assert 'Employment type' not in job['description_html']
    assert 'Information Technology and Services' not in job['description_html']


def test_spider_parse_job_no_company_link():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job_no_company_link.html').read_bytes())
    job = next(linkedin.Spider().parse_job(response)).cb_kwargs['item']

    assert job['company_name'] == 'Grafton Temporary Staffing'
    assert 'company_link' not in job
    assert job['locations_raw'] == ['Praha 4']


def test_spider_parse_job_applicants():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job_applicants.html').read_bytes())
    job = next(linkedin.Spider().parse_job(response)).cb_kwargs['item']

    assert job['posted_at'] == date.today()


def test_spider_parse_job_apply_on_company_website():
    response = HtmlResponse('https://example.com/example/',
                            body=Path(FIXTURES_DIR / 'job_apply_on_company_website.html').read_bytes())
    job = next(linkedin.Spider().parse_job(response)).cb_kwargs['item']

    assert job['link'] == 'https://jobs.cisco.com/jobs/ProjectDetail/Software-Engineer/1304909?source=juniorguru'


def test_clean_proxied_url():
    url = (
        'https://cz.linkedin.com/jobs/view/externalApply/2006390996'
        '?url=https%3A%2F%2Fjobs%2Egecareers%2Ecom%2Fglobal%2Fen%2Fjob%2FGE11GLOBAL32262%2FEngineering-Trainee%3Futm_source%3Dlinkedin%26codes%3DLinkedIn%26utm_medium%3Dphenom-feeds'
        '&urlHash=AAbh&refId=94017428-1cc1-48ad-bda2-d9ddabeb1c55&trk=public_jobs_apply-link-offsite'
    )

    assert linkedin.clean_proxied_url(url) == 'https://jobs.gecareers.com/global/en/job/GE11GLOBAL32262/Engineering-Trainee?codes=juniorguru'


def test_get_job_id():
    url = (
        'https://cz.linkedin.com/jobs/view/'
        'junior-software-engineer-at-cimpress-technology-2247016723'
    )

    assert linkedin.get_job_id(url) == '2247016723'


@pytest.mark.parametrize('url,expected', [
    ('https://uk.linkedin.com/company/adaptavist?trk=public_jobs_topcard_logo', 'https://uk.linkedin.com/company/adaptavist'),
    ('https://example.com?trk=123', 'https://example.com?trk=123'),
    ('https://pipedrive.talentify.io/job/junior-software-engineer-prague-prague-pipedrive-015b84ef-3956-4a28-877f-0385379d40c2?tdd=dDEsaDM1LGozdXFlZSxlcHJvNjA3ZjBhOTA2ZDVkNjE2OTQ4ODk3OA', 'https://pipedrive.talentify.io/job/junior-software-engineer-prague-prague-pipedrive-015b84ef-3956-4a28-877f-0385379d40c2'),
    ('https://neuvoo.cz/job.php?id=b5f15b6eeadc&source=juniorguru&puid=aadegddb8adaeddfeddb9ade7ddafadbaadbfadf3aeccacdfec3ddcg3e', 'https://neuvoo.cz/job.php?id=b5f15b6eeadc&source=juniorguru'),
    ('https://jobs.lever.co/pipedrive/015b84ef-3956-4a28-877f-0385379d40c2/apply', 'https://jobs.lever.co/pipedrive/015b84ef-3956-4a28-877f-0385379d40c2/'),
    ('https://erstegroup-careers.com/csas/job/Hlavn%C3%AD-m%C4%9Bsto-Praha-Tester-EOM/667861301/?locale=cs_CZ&utm_campaign=lilimitedlistings&utm_source=lilimitedlistings&applySourceOverride=Linkedin%20Limited%20Listings', 'https://erstegroup-careers.com/csas/job/Hlavn%C3%AD-m%C4%9Bsto-Praha-Tester-EOM/667861301/?locale=cs_CZ&applySourceOverride=juniorguru+Limited+Listings'),
])
def test_clean_url(url, expected):
    assert linkedin.clean_url(url) == expected


@pytest.mark.parametrize('text,expected', [
    ('Junior Software Engineer (C#.NET)', False),
    ('Remote Web Developer - Prague', True),
    ('Remote Web Developer', True),
])
def test_parse_remote(text, expected):
    assert linkedin.parse_remote(text) is expected
