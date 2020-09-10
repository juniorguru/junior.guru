from juniorguru.fetch.metrics import merge_metric_dicts


def test_merge_metric_dicts():
    assert merge_metric_dicts({
        'https://example.com/1/': 42,
        'https://example.com/100/': 420,
        'https://example.com/': 3,
    }, {
        'https://example.com/1/': 2,
        'https://example.com/4/': 10,
        'https://example.com/': 30,
    }) == {
        'https://example.com/1/': 44,
        'https://example.com/100/': 420,
        'https://example.com/4/': 10,
        'https://example.com/': 33,
    }
