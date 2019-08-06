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


def test_email_link_filter():
    markup = str(templating.email_link_filter('xyz@example.com'))
    assert markup == '<a href="mailto:xyz&#64;example.com">xyz&#64;<!---->example.com</a>'


def test_email_link_filter_using_text_template():
    text_template = 'gargamel {email} smurf'
    markup = str(templating.email_link_filter('xyz@example.com', text_template))
    assert markup == '<a href="mailto:xyz&#64;example.com">gargamel xyz&#64;<!---->example.com smurf</a>'


def test_markdown_filter():
    markup = str(templating.markdown_filter('call me **maybe**  \ncall me Honza'))
    assert markup == '<p>call me <strong>maybe</strong><br>\ncall me Honza</p>'
