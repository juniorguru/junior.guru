import pytest

from juniorguru.lib import loggers


@pytest.mark.parametrize('path, expected', [
    ('/a/b/c/juniorguru/juniorguru/sync/club_content/__init__.py', 'juniorguru.sync.club_content'),
    ('/a/b/c/juniorguru/juniorguru/sync/club_content/crawler.py', 'juniorguru.sync.club_content.crawler'),
])
def test_from_path(path, expected):
    assert loggers.from_path(path, cwd='/a/b/c/juniorguru').name == expected


@pytest.mark.parametrize('key, expected', [
    (123, 'name.123'),
    ('abc', 'name.abc'),
])
def test_getitem(key, expected):
    assert loggers.get('name')[key].name == expected
