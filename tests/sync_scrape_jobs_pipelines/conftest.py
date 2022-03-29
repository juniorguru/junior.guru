from datetime import date

import pytest
from scrapy import Spider

from juniorguru.sync.scrape_jobs.items import Job


@pytest.fixture
def item():
    return Job(
        title='Junior Python Engineer',
        first_seen_on=date.today(),
        url='https://example.com/jobs/123',
        company_name='Mergado',
        employment_types=['full-time'],
        description_html='...',
        source='startupjobs',
        source_urls=['https://www.startupjobs.cz/nabidka/38100/python-backend-developer-brno'],
    )


@pytest.fixture
def spider():
    class DummySpider(Spider):
        name = 'dummy'

    return DummySpider()
