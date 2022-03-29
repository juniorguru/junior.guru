from operator import itemgetter

import pytest

from juniorguru.jobs.legacy_jobs.pipelines import locations


def test_locations(item, spider):
    address = {'place': 'Řevnice',
               'region': 'Středočeský kraj',
               'country': 'Česko'}
    item['locations_raw'] = ['252 30 Řevnice, Česko']
    item = locations.Pipeline(geocode=lambda l: address).process_item(item, spider)

    assert item['locations'] == [{'name': 'Řevnice', 'region': 'Praha'}]


def test_locations_remote(item, spider):
    item['locations_raw'] = []
    item = locations.Pipeline(geocode=lambda l: {}).process_item(item, spider)

    assert item.get('locations', []) == []


def test_locations_no_response(item, spider):
    item['locations_raw'] = ['???']
    item = locations.Pipeline(geocode=lambda l: None).process_item(item, spider)

    assert item.get('locations', []) == []


def test_locations_multiple(item, spider):
    addresses = iter([
        {'place': 'Řevnice',
         'region': 'Středočeský kraj',
         'country': 'Česko'},
        {'place': 'Brno',
         'region': 'Jihomoravský kraj',
         'country': 'Česko'}
    ])
    item['locations_raw'] = ['252 30 Řevnice, Česko', 'Brno, Česko']
    item = locations.Pipeline(geocode=lambda l: next(addresses)).process_item(item, spider)

    assert sorted(item['locations'], key=itemgetter('name')) == [
        {'name': 'Brno', 'region': 'Brno'},
        {'name': 'Řevnice', 'region': 'Praha'},
    ]


def test_locations_multiple_no_response(item, spider):
    addresses = iter([
        None,
        {'place': 'Brno',
         'region': 'Jihomoravský kraj',
         'country': 'Česko'}
    ])
    item['locations_raw'] = ['???', 'Brno, Česko']
    item = locations.Pipeline(geocode=lambda l: next(addresses)).process_item(item, spider)

    assert item['locations'] == [{'name': 'Brno', 'region': 'Brno'}]


def test_locations_multiple_unique(item, spider):
    addresses = iter([
        {'place': 'Brno',
         'region': 'Jihomoravský kraj',
         'country': 'Česko'},
        {'place': 'Brno',
         'region': 'Jihomoravský kraj',
         'country': 'Česko'}
    ])
    item['locations_raw'] = ['Plevova 1, Brno, Česko', 'Brno, Česko']
    item = locations.Pipeline(geocode=lambda l: next(addresses)).process_item(item, spider)

    assert item['locations'] == [{'name': 'Brno', 'region': 'Brno'}]


def test_get_region_from_country():
    address = dict(region='Województwo Mazowieckie',
                   country='Polska')

    assert locations.get_region(address) == 'Polsko'


@pytest.mark.parametrize('country', [
    'Česko',
    'Česká republika',
])
def test_get_region_from_region(country):
    address = dict(region='Středočeský kraj',
                   country=country)

    assert locations.get_region(address) == 'Praha'


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

    assert locations.optimize_geocoding(geocode)(location_raw) == expected
