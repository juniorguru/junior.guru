from juniorguru.lib.proxies import ScrapingProxiesMiddleware

import pytest


@pytest.fixture()
def proxies_list():
    return ['http://example.com:1',
            'http://example.com:2',
            'http://example.com:3',
            'http://example.com:4',
            'http://example.com:5']


@pytest.fixture()
def middleware(proxies_list):
    return ScrapingProxiesMiddleware(proxies_list, enabled=True)
