from datetime import date

import pytest
from scrapy import Spider


@pytest.fixture
def item():
    return dict(
        title='Junior Python Engineer',
        company_name='The Best Company',
        locations=[{'name': 'Tečovice', 'region': 'Zlín'}],
        urls=['https://example.com/jobs/123'],
        description_html='<p>Need Pythonistas!</p>',
        lang='en',
        seen_at=date.today(),
        source='example-job-board',
        source_urls=['https://example.com/jobs/'],
    )


@pytest.fixture
def spider():
    class ExampleSpider(Spider):
        name = 'example'

    return ExampleSpider()
