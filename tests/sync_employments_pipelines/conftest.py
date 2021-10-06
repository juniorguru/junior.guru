from datetime import date, timedelta

import pytest
from scrapy import Spider


@pytest.fixture
def item():
    return dict(
        title='Junior Python Engineer',
        company_name='The Best Company',
        locations=[{'name': 'Tečovice', 'region': 'Zlín'}],
        remote=True,
        url='https://example.com/jobs/123',
        external_ids=[],
        description_html='<p>Need Pythonistas!</p>',
        description_text='Need Pythonistas!',
        lang='en',
        first_seen_at=date.today() - timedelta(days=3),
        last_seen_at=date.today(),
        employment_types=['FULL_TIME'],
        source='example-job-board',
        source_urls=['https://example.com/jobs/'],
    )


@pytest.fixture
def spider():
    class ExampleSpider(Spider):
        name = 'example'

    return ExampleSpider()
