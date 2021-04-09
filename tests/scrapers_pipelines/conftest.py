from datetime import date, timedelta

import pytest
from scrapy import Spider


@pytest.fixture
def item():
    return dict(
        id='44df50581c3a0c67657c40a587c22a19e10d414b593fcfaea5b01ae9',
        posted_at=date.today(),
        expires_at=date.today() + timedelta(days=30),
        title='Junior Python Engineer',
        remote=True,
        company_name='The Best Company',
        company_link='https://example.com',
        employment_types=['full-time'],
        description_html='...',
        link='https://example.com/jobs/123',
        junior_rank=10,
        sort_rank=5,
        lang='cs',
    )


@pytest.fixture
def spider():
    class DummySpider(Spider):
        name = 'dummy'

    return DummySpider()
