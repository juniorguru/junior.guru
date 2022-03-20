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


def test_calc_avg_latency(middleware):
    middleware.LATENCIES_SAMPLE_SIZE = 4

    assert middleware.calc_avg_latency([5, 6, 30, 9, 1, 100, 8, 3]) == 28


def test_get_proxies_with_avg_latency(middleware):
    middleware.POOL_SIZE = 10
    middleware.record_proxy_latency('http://example.com:2', 2)
    middleware.record_proxy_latency('http://example.com:2', 100)
    middleware.record_proxy_latency('http://example.com:3', 10)
    middleware.record_proxy_latency('http://example.com:5', 5)
    middleware.record_proxy_latency('http://example.com:5', 1)

    assert set(middleware.get_proxies_with_avg_latency()) == {('http://example.com:5', 3.0),
                                                              ('http://example.com:3', 10.0),
                                                              ('http://example.com:2', 51.0)}


@pytest.mark.skip
def test_get_proxies_with_avg_latency_skips_timeouting_proxies(middleware):
    middleware.POOL_SIZE = 10

    # multiple values, timeouting
    middleware.record_proxy_latency('http://example.com:1', middleware.TIMEOUT_LATENCY)
    middleware.record_proxy_latency('http://example.com:1', middleware.TIMEOUT_LATENCY)

    # low latency
    middleware.record_proxy_latency('http://example.com:2', 2)
    middleware.record_proxy_latency('http://example.com:3', 3)

    # single value, timeouting
    middleware.record_proxy_latency('http://example.com:4', middleware.TIMEOUT_LATENCY)

    # timeouting just once, otherwise low latency
    middleware.record_proxy_latency('http://example.com:5', 5)
    middleware.record_proxy_latency('http://example.com:5', middleware.TIMEOUT_LATENCY)
    middleware.record_proxy_latency('http://example.com:5', 5)
    middleware.record_proxy_latency('http://example.com:5', 5)

    assert set(middleware.get_proxies_with_avg_latency()) == {('http://example.com:2', 2.0),
                                                              ('http://example.com:3', 3.0),
                                                              ('http://example.com:5', ((5 + 5 + 5 + middleware.TIMEOUT_LATENCY) / 4))}


def test_get_low_latency_proxies_sorts_by_avg_latency(middleware):
    middleware.POOL_SIZE = 10
    middleware.record_proxy_latency('http://example.com:2', 2)
    middleware.record_proxy_latency('http://example.com:2', 100)
    middleware.record_proxy_latency('http://example.com:3', 3)
    middleware.record_proxy_latency('http://example.com:3', 10)
    middleware.record_proxy_latency('http://example.com:5', 5)
    middleware.record_proxy_latency('http://example.com:5', 500)

    assert middleware.get_low_latency_proxies() == ['http://example.com:3',
                                                    'http://example.com:2',
                                                    'http://example.com:5']


def test_get_low_latency_proxies_returns_max_pool_size_items(middleware):
    middleware.POOL_SIZE = 2
    middleware.record_proxy_latency('http://example.com:2', 2)
    middleware.record_proxy_latency('http://example.com:3', 3)
    middleware.record_proxy_latency('http://example.com:5', 5)

    assert middleware.get_low_latency_proxies() == ['http://example.com:2',
                                                    'http://example.com:3']


def test_get_proxy_pool(middleware):
    middleware.POOL_SIZE = 10
    pool = middleware.get_proxy_pool()

    assert set(pool) == {'http://example.com:1',
                         'http://example.com:2',
                         'http://example.com:3',
                         'http://example.com:4',
                         'http://example.com:5'}


def test_get_proxy_pool_returns_only_low_latency_proxies_if_enough(middleware):
    middleware.POOL_SIZE = 2
    middleware.record_proxy_latency('http://example.com:2', 2)
    middleware.record_proxy_latency('http://example.com:3', 3)
    middleware.record_proxy_latency('http://example.com:5', 5)

    assert middleware.get_proxy_pool() == ['http://example.com:2',
                                           'http://example.com:3']


@pytest.mark.skip
def test_get_proxy_pool_skips_timeouting_proxies(middleware):
    middleware.POOL_SIZE = 10
    middleware.record_proxy_latency('http://example.com:1', middleware.TIMEOUT_LATENCY)
    middleware.record_proxy_latency('http://example.com:1', middleware.TIMEOUT_LATENCY)
    middleware.record_proxy_latency('http://example.com:2', 2)
    middleware.record_proxy_latency('http://example.com:3', 3)
    middleware.record_proxy_latency('http://example.com:4', middleware.TIMEOUT_LATENCY)
    middleware.record_proxy_latency('http://example.com:5', 5)

    pool = middleware.get_proxy_pool()

    assert pool == ['http://example.com:2',
                    'http://example.com:3',
                    'http://example.com:5']


def test_get_proxy_pool_backfills_with_random_proxies_without_known_latencies(middleware):
    middleware.POOL_SIZE = 10
    middleware.record_proxy_latency('http://example.com:2', 2)
    middleware.record_proxy_latency('http://example.com:3', 3)
    middleware.record_proxy_latency('http://example.com:5', 5)
    pool = middleware.get_proxy_pool()

    assert pool[:3] == ['http://example.com:2',
                        'http://example.com:3',
                        'http://example.com:5']
    assert set(pool[3:]) == {'http://example.com:1',
                             'http://example.com:4'}
