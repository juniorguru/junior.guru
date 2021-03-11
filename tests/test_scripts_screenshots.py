import pytest

from scripts import screenshots


@pytest.mark.parametrize('url,expected', [
    ('https://example.com', 'https://example.com'),
    ('https://example.com/foo/', 'https://example.com/foo'),
    ('https://junior.guru/club/', 'http://localhost:5000/club'),
    ('https://junior.guru/learn/#english', 'http://localhost:5000/learn/#english'),
])
def test_parse_url(url, expected):
    assert screenshots.parse_url(url) == expected
