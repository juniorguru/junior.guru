import itertools
import json

from pathlib import Path
import pytest

from juniorguru.sync.meetups import parse_icalendar, parse_json_dl, parse_json_dl_location


@pytest.fixture
def icalendar_content():
    return (Path(__file__).parent / 'pyvo.ics').read_text()


@pytest.fixture
def json_dl_content():
    return (Path(__file__).parent / 'json_dl.html').read_text()


def test_parse_json_dl_location():
    json_dl = ('{"@type":"Place","name":"Mews","address":{"@type":"PostalAddress",'
               '"addressLocality":"Praha-Praha 2","addressCountry":"Czech Republic",'
               '"streetAddress":"nám. I. P. Pavlova 5, Vinohrady"},"geo":{"@type":"GeoCoordinates",'
               '"latitude":50.07499694824219,"longitude":14.429851531982422}}')
    json_dl_location = json.loads(json_dl)

    assert parse_json_dl_location(json_dl_location) == 'Mews, nám. I. P. Pavlova 5, Vinohrady, Praha-Praha 2, Czech Republic'


def test_parse_icalendar(icalendar_content):
    events = parse_icalendar(icalendar_content)
    keys = set(itertools.chain.from_iterable(event.keys() for event in events))

    assert keys == {'name_raw', 'starts_at', 'location_raw', 'url'}


def test_parse_json_dl(json_dl_content):
    events = parse_json_dl(json_dl_content, 'https://www.meetup.com/reactgirls/events/')
    keys = set(itertools.chain.from_iterable(event.keys() for event in events))

    assert keys == {'name_raw', 'starts_at', 'location_raw', 'url'}
