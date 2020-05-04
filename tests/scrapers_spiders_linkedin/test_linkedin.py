import pytest

from juniorguru.scrapers.spiders import linkedin


@pytest.mark.parametrize('url,param_names,expected', [
    ('https://example.com', ['a', 'b'], 'https://example.com'),
    ('https://example.com?a=1&b=2', ['a', 'b'], 'https://example.com'),
    ('https://example.com?a=1&c=3&b=2', ['a', 'b'], 'https://example.com?c=3'),
    ('https://example.com', [], 'https://example.com'),
    ('https://example.com?a=1&b=2', [], 'https://example.com?a=1&b=2'),
])
def test_strip_params(url, param_names, expected):
    assert linkedin.strip_params(url, param_names) == expected
