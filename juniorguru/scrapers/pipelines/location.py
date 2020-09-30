import geopy

from juniorguru.scrapers.settings import USER_AGENT


REGIONS_MAPPING = {
    # countries
    'Deutchland': 'Německo',
    'Polska': 'Polsko',
    'Österreich': 'Rakousko',

    # regions
    'Hlavní město Praha': 'Praha',
    'Středočeský kraj': 'Praha',
    'Jihočeský kraj': 'České Budějovice',
    'Plzeňský kraj': 'Plzeň',
    'Karlovarský kraj': 'Karlovy Vary',
    'Ústecký kraj': 'Ústí nad Labem',
    'Liberecký kraj': 'Liberec',
    'Královéhradecký kraj': 'Hradec Králové',
    'Pardubický kraj': 'Pardubice',
    'Olomoucký kraj': 'Olomouc',
    'Moravskoslezský kraj': 'Ostrava',
    'Jihomoravský kraj': 'Brno',
    'Zlínský kraj': 'Zlín',
    'Kraj Vysočina': 'Jihlava',
}


class Pipeline():
    def __init__(self, stats=None, geocode=None):
        self.stats = stats
        self.geocode = geocode or geocode_osm

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

    def process_item(self, item, spider):
        if item.get('location'):
            location = item['location']
            address = self.geocode(location)
            if address:
                try:
                    item['region'] = get_region(address)
                    item['location_place'] = get_place(address)
                    item['location_country_code'] = address['country_code'].upper()
                except KeyError as e:
                    raise KeyError(f"{address!r} doesn't have key {e} ({location})")
                if self.stats:
                    self.stats.inc_value('item_geocoded_count')
        return item


def geocode_osm(location):
    geolocator = geopy.geocoders.Nominatim(user_agent=USER_AGENT)
    response = geolocator.geocode(location, addressdetails=True)
    if response:
        return response.raw['address']
    return None


def get_place(address):
    return next(filter(None, [
        address.get('city'),
        address.get('village'),
    ]))


def get_region(address):
    if address['country_code'].upper() == 'CZ':
        region = address['county']
    else:
        region = address['country']
    return REGIONS_MAPPING.get(region, region)


if __name__ == "__main__":
    # python -m juniorguru.scrapers.pipelines.location 'Brno, South Moravia, Czech Republic'
    import sys
    from pprint import pprint
    pprint(geocode_osm(sys.argv[1]))
