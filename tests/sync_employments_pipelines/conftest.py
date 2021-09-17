from datetime import date

import pytest
from scrapy import Spider


@pytest.fixture
def item():
    return dict(
        id='44df50581c3a0c67657c40a587c22a19e10d414b593fcfaea5b01ae9',
        title='Junior Python Engineer',
        company_name='The Best Company',
        url='https://example.com/jobs/123',
        description_html='...',
        seen_at=date.today(),
        source='example-job-board',
        source_url='https://example.com/jobs/',
    )


@pytest.fixture
def spider():
    class ExampleSpider(Spider):
        name = 'example'

    return ExampleSpider()
