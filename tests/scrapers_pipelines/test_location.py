import pytest

from juniorguru.scrapers.pipelines.location import Pipeline, get_region


def test_location(item, spider):
    address = dict(place='Řevnice',
                   region='Středočeský kraj',
                   country='Česko')
    item['location_raw'] = '252 30 Řevnice, Česko'
    item = Pipeline(geocode=lambda l: address).process_item(item, spider)

    assert item['region'] == 'Praha'
    assert item['location_place'] == 'Řevnice'
    assert item['location_country'] == 'Česko'


def test_location_remote(item, spider):
    item['location_raw'] = None
    item = Pipeline(geocode=lambda l: {}).process_item(item, spider)

    assert item.get('region') is None
    assert item.get('location_place') is None
    assert item.get('location_country') is None


def test_location_no_response(item, spider):
    item['location_raw'] = '???'
    item = Pipeline(geocode=lambda l: None).process_item(item, spider)

    assert item.get('region') is None
    assert item.get('location_place') is None
    assert item.get('location_country') is None


def test_get_region_from_country():
    address = dict(region='Województwo Mazowieckie',
                   country='Polska')

    assert get_region(address) == 'Polsko'


@pytest.mark.parametrize('country', [
    'Česko',
    'Česká republika',
])
def test_get_region_from_region(country):
    address = dict(region='Středočeský kraj',
                   country=country)

    assert get_region(address) == 'Praha'
