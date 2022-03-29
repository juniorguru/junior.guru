import pytest

from juniorguru.sync.jobs_scraped.pipelines.company_url_cleaner import process


@pytest.mark.parametrize('company_url, expected', [
    ('https://www.linkedin.com/company/fakturoid/', None),
    ('https://www.fakturoid.cz/', 'https://www.fakturoid.cz/'),
])
def test_company_url_cleaner(company_url, expected):
    item = process(dict(company_url=company_url))

    assert item['company_url'] == expected
