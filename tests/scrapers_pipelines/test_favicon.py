from pathlib import Path

import responses

from juniorguru.scrapers.pipelines.favicon import get_favicons


@responses.activate
def test_redhat():
    fixture_path = Path(__file__).parent / 'fixtures_favicon' / 'specimen_redhat.html'
    responses.add(responses.GET, 'https://example.com', body=fixture_path.read_text())
    responses.add(responses.HEAD, 'https://example.com/favicon.ico')

    assert set(get_favicons('https://example.com')) == {
        'https://example.com/favicon.ico',
        'https://www.redhat.com/profiles/rh/themes/redhatdotcom/img/red-hat-social-share.jpg',
        'https://www.redhat.com/misc/favicon.ico',
    }


@responses.activate
def test_inizio():
    fixture_path = Path(__file__).parent / 'fixtures_favicon' / 'specimen_inizio.html'
    responses.add(responses.GET, 'https://example.com', body=fixture_path.read_text())
    responses.add(responses.HEAD, 'https://example.com/favicon.ico', status=404)

    assert set(get_favicons('https://example.com')) == {
        'https://www.inizio.cz/page/img/favicon.ico?v=402',
        'https://www.inizio.cz/galerie/tinymce/inizio_fb.png',
    }
