import pytest

from juniorguru.scrapers import items


@pytest.mark.parametrize('string,expected', [
    ('', []),
    ('       , ', []),
    ('a,b,,c,', ['a', 'b', 'c']),
    ('  a,     b ,  ', ['a', 'b']),
])
def test_split(string, expected):
    assert items.split(string) == expected


def test_split_by():
    assert items.split('a-b , -  - c-', by='-') == ['a', 'b ,', 'c']
