import pytest

from juniorguru.scrapers.pipelines import location


def test_location(item, spider):
    address = dict(place='Řevnice',
                   region='Středočeský kraj',
                   country='Česko')
    item['location_raw'] = '252 30 Řevnice, Česko'
    item = location.Pipeline(geocode=lambda l: address).process_item(item, spider)

    assert item['region'] == 'Praha'
    assert item['location_place'] == 'Řevnice'


def test_location_remote(item, spider):
    item['location_raw'] = None
    item = location.Pipeline(geocode=lambda l: {}).process_item(item, spider)

    assert item.get('region') is None
    assert item.get('location_place') is None


def test_location_no_response(item, spider):
    item['location_raw'] = '???'
    item = location.Pipeline(geocode=lambda l: None).process_item(item, spider)

    assert item.get('region') is None
    assert item.get('location_place') is None


def test_get_region_from_country():
    address = dict(region='Województwo Mazowieckie',
                   country='Polska')

    assert location.get_region(address) == 'Polsko'


@pytest.mark.parametrize('country', [
    'Česko',
    'Česká republika',
])
def test_get_region_from_region(country):
    address = dict(region='Středočeský kraj',
                   country=country)

    assert location.get_region(address) == 'Praha'


GEOCODED_ADDRESS = {'place': '-- GEOCODED --',
                    'region': '-- GEOCODED --',
                    'country': '-- GEOCODED --'}


@pytest.mark.parametrize('location_raw,expected', [
    ('252 30 Řevnice, Česko',
     GEOCODED_ADDRESS),
    ('130 00 Praha 3-Žižkov',
     {'place': 'Praha', 'region': 'Praha', 'country' :'Česko'}),
    ('Prague, Czechia',
     {'place': 'Praha', 'region': 'Praha', 'country' :'Česko'}),
    ('Brno-Žabovřesky',
     {'place': 'Brno', 'region': 'Brno', 'country' :'Česko'}),
    ('Michálkovická 1137/197, 710 00 Ostrava - Slezská Ostrava, Czechia',
     {'place': 'Ostrava', 'region': 'Ostrava', 'country' :'Česko'}),
])
def test_optimize_geocoding(location_raw, expected):
    def geocode(location_raw):
        return GEOCODED_ADDRESS

    assert location.optimize_geocoding(geocode)(location_raw) == expected
