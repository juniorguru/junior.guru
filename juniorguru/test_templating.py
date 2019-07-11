import pytest

from juniorguru import templating


@pytest.mark.parametrize('url_path,url', [
    ('/', 'https://example.com'),
    ('/foo/bar', 'https://example.com/foo/bar'),
    ('foo/bar', 'https://example.com/foo/bar'),
    ('foo.html', 'https://example.com/foo.html'),
])
def test_get_url(url_path, url):
    assert templating.get_url('https://example.com/', url_path) == url


@pytest.mark.parametrize('url_path,html_path', [
    ('/', '/tmp/build/index.html'),
    ('/index.html', '/tmp/build/index.html'),
    ('/foo', '/tmp/build/foo/index.html'),
    ('/foo/', '/tmp/build/foo/index.html'),
    ('/foo/index.html', '/tmp/build/foo/index.html'),
])
def test_get_html_path(url_path, html_path):
    assert str(templating.get_html_path('/tmp/build', url_path)) == html_path
