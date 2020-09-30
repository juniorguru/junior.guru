import pytest

from juniorguru.scrapers.pipelines.region_parser import Pipeline, detect_region


@pytest.mark.parametrize('location,expected_region', [
    ('Brno', 'Brno'),
    ('Brno, Czech Republic', 'Brno'),
    ('Praha, Česko', 'Praha'),
    ('Praha 1, Česko', 'Praha'),
    ('Praha 8, Czechia', 'Praha'),
    ('252 30 Řevnice, Česko', None),
    ('130 00 Praha 3, Česko', 'Praha'),
    ('Ostrava, Moravia-Silesia, Czech Republic', 'Ostrava'),
    ('Káranice, Hradec Králové, Czech Republic', 'Hradec Králové'),
    ('Bratislava, Slovensko', 'Slovensko'),
])
def test_detect_region(location, expected_region):
    assert detect_region(location) == expected_region


def test_region_parser_detectable(item, spider):
    item['location'] = 'Praha'
    item = Pipeline().process_item(item, spider)

    assert item['region'] == 'Praha'


def test_region_parser_detectable_and_geocoding_set(item, spider):
    item['location'] = 'Praha'
    item = Pipeline(geocode=lambda l: 'Krakozhia').process_item(item, spider)

    assert item['region'] == 'Praha'


def test_region_parser_not_detectable(item, spider):
    item['location'] = 'Lázně Toušeň'
    item = Pipeline().process_item(item, spider)

    assert item['region'] is None


def test_region_parser_not_detectable_but_geocoding_set(item, spider):
    item['location'] = 'Lázně Toušeň'
    item = Pipeline(geocode=lambda l: 'Krakozhia').process_item(item, spider)

    assert item['region'] == 'Krakozhia'
