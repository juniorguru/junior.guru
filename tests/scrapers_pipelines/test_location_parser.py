import pytest

from juniorguru.scrapers.pipelines.location_parser import Pipeline, parse_location


@pytest.mark.parametrize('location,expected_country,expected_region', [
    ('Brno', None, 'Brno'),
    ('Brno, Czech Republic', 'Česko', 'Brno'),
    ('Praha, Česko', 'Česko', 'Praha'),
    ('Praha 1, Česko', 'Česko', 'Praha'),
    ('Praha 8, Czechia', 'Česko', 'Praha'),
    ('252 30 Řevnice, Česko', 'Česko', None),
    ('130 00 Praha 3, Česko', 'Česko', 'Praha'),
    ('Ostrava, Moravia-Silesia, Czech Republic', 'Česko', 'Ostrava'),
    ('Káranice, Hradec Králové, Czech Republic', 'Česko', 'Hradec Králové'),
])
def test_parse_location(location, expected_country, expected_region):
    assert parse_location(location) == (expected_country, expected_region)


def test_location_parser(item, spider):
    item['location'] = 'Bratislava, Slovensko'
    item = Pipeline().process_item(item, spider)

    assert item['location_region'] == None
    assert item['location_country'] == 'Slovensko'


def test_location_parser_no_region(item, spider):
    item['location'] = 'Pavčina Lehota, Slovensko'
    item = Pipeline().process_item(item, spider)

    assert item['location_region'] == None
    assert item['location_country'] == 'Slovensko'


def test_location_parser_respects_default_country_spider_attribute(item, spider):
    spider.default_country = 'Krakozhia'
    item['location'] = 'Pavčina Lehota'
    item = Pipeline().process_item(item, spider)

    assert item['location_region'] == None
    assert item['location_country'] == 'Krakozhia'


def test_location_parser_sets_cze_as_default_country(item, spider):
    spider.default_country = None
    item['location'] = 'Lázně Toušeň'
    item = Pipeline().process_item(item, spider)

    assert item['location_region'] == None
    assert item['location_country'] == 'Česko'
