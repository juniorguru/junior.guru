from datetime import datetime

import pytest
from scrapy import Spider


@pytest.fixture
def item():
    return dict(
        posted_at=datetime.utcnow(),
        title='Junior Python Engineer',
        location='Brno, Czechia',
        company_name='The Best Company',
        company_link='https://example.com',
        employment_types=['full-time'],
        description_raw='...',
        link='https://example.com/jobs/123',
    )


@pytest.fixture
def spider():
    class DummySpider(Spider):
        name = 'dummy'

    return DummySpider()
