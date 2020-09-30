from juniorguru.scrapers.pipelines.location import Pipeline, get_region


def test_location(item, spider):
    address = dict(city='Řevnice',
                   county='Středočeský kraj',
                   country_code='cz')
    item['location'] = '252 30 Řevnice, Česko'
    item = Pipeline(geocode=lambda l: address).process_item(item, spider)

    assert item['region'] == 'Praha'
    assert item['location_city'] == 'Řevnice'
    assert item['location_country_code'] == 'CZ'


def test_location_remote(item, spider):
    item['location'] = None
    item = Pipeline(geocode=lambda l: {}).process_item(item, spider)

    assert item.get('region') is None
    assert item.get('location_city') is None
    assert item.get('location_country_code') is None


def test_get_region_country():
    address = dict(county='Województwo Mazowieckie',
                   country='Polska',
                   country_code='pl')

    assert get_region(address) == 'Polsko'


def test_get_region_county():
    address = dict(county='Středočeský kraj',
                   country='Česká republika',
                   country_code='cz')

    assert get_region(address) == 'Praha'
