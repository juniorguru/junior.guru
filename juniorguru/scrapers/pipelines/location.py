import re
from functools import lru_cache, wraps

import requests
from lxml import etree

from juniorguru.lib.log import get_log
from juniorguru.scrapers.settings import USER_AGENT


log = get_log(__name__)


class GeocodeError(Exception):
    pass


OPTIMIZATIONS = [
    (re.compile(pattern), value) for pattern, value in [
        (r'\bPraha\b', {'place': 'Praha', 'region': 'Praha', 'country': 'Česko'}),
        (r'\bPrague\b', {'place': 'Praha', 'region': 'Praha', 'country': 'Česko'}),
        (r'\bBrno\b', {'place': 'Brno', 'region': 'Brno', 'country': 'Česko'}),
        (r'\bOstrava\b', {'place': 'Ostrava', 'region': 'Ostrava', 'country': 'Česko'}),
    ]
]
REGIONS_MAPPING = {
    # countries
    'Deutschland': 'Německo',
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
ADDRESS_TYPES_MAPPING = {
    # Mapy.cz
    'muni': 'place',
    'regi': 'region',
    'coun': 'country',

    # OpenStreetMaps
    'osmm': 'place',
    'osmr': 'region',
    'osmc': 'country',
}


class Pipeline():
    def __init__(self, stats=None, geocode=None):
        self.stats = stats
        self.geocode = geocode or geocode_mapycz

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

    def process_item(self, item, spider):
        if item.get('location_raw'):
            location_raw = item['location_raw']
            try:
                log.debug(f"Geocoding '{location_raw}'")
                address = self.geocode(location_raw)
                if address:
                    try:
                        item['region'] = get_region(address)
                        item['location_place'] = address['place']
                    except KeyError as e:
                        raise KeyError(f"{address!r} doesn't have key {e}") from e
                    if self.stats:
                        self.stats.inc_value('item_geocoded_count')
            except Exception:
                info = dict(spider=spider.name,
                            title=item.get('title'),
                            company=item.get('company_name'))
                log.exception(f"Geocoding '{location_raw}' failed, {info!r}")
        return item


def optimize_geocoding(geocode):
    @wraps(geocode)
    def wrapper(location_raw):
        for location_re, value in OPTIMIZATIONS:
            if location_re.search(location_raw):
                return value
        return lru_cache(geocode)(location_raw)
    return wrapper


@optimize_geocoding
def geocode_mapycz(location_raw):
    try:
        response = requests.get('https://api.mapy.cz/geocode',
                                params={'query': location_raw},
                                headers={'User-Agent': USER_AGENT})
        response.raise_for_status()

        xml = etree.fromstring(response.content)
        items = xml.xpath('//item')
        if not items:
            return None

        item = items[0]
        title, lat, lng = item.get('title'), item.get('y'), item.get('x')
    except requests.RequestException as e:
        raise GeocodeError(f"Unable to geocode '{location_raw}'") from e

    try:
        response = requests.get('https://api.mapy.cz/rgeocode',
                                params={'lat': lat, 'lon': lng},
                                headers={'User-Agent': USER_AGENT})
        response.raise_for_status()

        xml = etree.fromstring(response.content)
        items = xml.xpath('//item')
        if not items:
            raise ValueError('No items in the reverse geocode response')

        address = {ADDRESS_TYPES_MAPPING[item.attrib['type']]: item.attrib['name']
                   for item in items if item.attrib['type'] in ADDRESS_TYPES_MAPPING}
        return address
    except requests.RequestException as e:
        raise GeocodeError(f"Unable to geocode '{location_raw}' (unable to reverse geocode '{title}' lat: {lat} lng: {lng})") from e


def get_region(address):
    if address['country'].lower().startswith('česk'):
        region = address['region']
    else:
        region = address['country']
    return REGIONS_MAPPING.get(region, region)


if __name__ == '__main__':
    """
    Usage:

        python -m juniorguru.scrapers.pipelines.location 'Brno, South Moravia'
    """
    import sys
    from pprint import pprint
    from collections import namedtuple

    location_raw = sys.argv[1]
    print('Pipeline().geocode()')
    pprint(Pipeline().geocode(location_raw))
    print('---\nPipeline().process_item()')
    spider = namedtuple('Spider', ['name'])(name='test')
    pprint(Pipeline().process_item({'location_raw': location_raw}, spider))
