import pytest
from scrapy import Spider

from juniorguru.jobs.legacy_jobs.monitoring import get_response_data


@pytest.fixture
def spider():
    class DummySpider(Spider):
        name = 'dummy'

    return DummySpider()


def test_get_response_data(spider):
    data = get_response_data(spider, 'https://example.com')

    assert list(data.keys()) == ['response_url', 'response_backup_path']
    assert data['response_url'] == 'https://example.com'
    assert str(data['response_backup_path']).endswith('.txt')


@pytest.mark.parametrize('url', [
    None,
    'https://override.example.com',
])
def test_get_response_data_override_response_url(spider, url):
    spider.override_response_url = url
    data = get_response_data(spider, 'https://example.com')

    assert list(data.keys()) == ['response_url', 'response_backup_path']
    assert data['response_url'] == url
    assert str(data['response_backup_path']).endswith('.txt')


@pytest.mark.parametrize('path', [
    None,
    '/foo/moo/boo.xyz',
])
def test_get_response_data_override_response_backup_path(spider, path):
    spider.override_response_backup_path = path
    data = get_response_data(spider, 'https://example.com')

    assert list(data.keys()) == ['response_url', 'response_backup_path']
    assert data['response_url'] == 'https://example.com'
    assert data['response_backup_path'] == path
