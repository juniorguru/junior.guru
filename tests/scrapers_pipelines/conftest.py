from datetime import date

import pytest
from scrapy import Spider


@pytest.fixture
def item():
    return dict(
        posted_at=date.today(),
        title='Junior Python Engineer',
        location='Brno, Czechia',
        company_name='The Best Company',
        company_link='https://example.com',
        employment_types=['full-time'],
        description_html='...',
        link='https://example.com/jobs/123',
        junior_rank=10,
        lang='cs',
    )


@pytest.fixture
def spider():
    class DummySpider(Spider):
        name = 'dummy'

    return DummySpider()
