import pytest

from juniorguru.lib import loggers


@pytest.mark.parametrize('path, expected', [
    ('/a/b/c/juniorguru/juniorguru/sync/club_content/__init__.py', 'juniorguru.sync.club_content'),
    ('/a/b/c/juniorguru/juniorguru/sync/club_content/crawler.py', 'juniorguru.sync.club_content.crawler'),
])
def test_is_image_mimetype(path, expected):
    assert loggers.from_path(path, cwd='/a/b/c/juniorguru').name == expected
