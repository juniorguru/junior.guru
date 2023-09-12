import re
from functools import lru_cache, wraps

import requests
from lxml import etree

from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


# https://docs.python-requests.org/en/master/user/advanced/#timeouts
MAPYCZ_REQUEST_TIMEOUT = (3.05, 27)

# Seznam has silently turned off access to the original API.
# This is a HOTFIX with values from the example at https://api.mapy.cz/view?page=geocoding.
# I've contacted Seznam support meanwhile to get proper access to the new API.
MAPYCZ_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.8,cs;q=0.6,sk;q=0.4,es;q=0.2",
    "Referer": "https://fiddle.jshell.net/",
    "X-SZN-Sdk": "HgUbCgUbGkgqAQkYBxYEHQNHQlJcSlBYSlJbQg==",
    "X-Mapy-Api-Key": "virtual-0fcd17d444befc9b4fa678d506bafc5b",
}

OPTIMIZATIONS = [
    (re.compile(pattern, re.I), value)
    for pattern, value in [
        (r"\bpraha\b", {"place": "Praha", "region": "Praha", "country": "Česko"}),
        (r"\bprague\b", {"place": "Praha", "region": "Praha", "country": "Česko"}),
        (r"\bbrno\b", {"place": "Brno", "region": "Brno", "country": "Česko"}),
        (r"\bostrava\b", {"place": "Ostrava", "region": "Ostrava", "country": "Česko"}),
        (
            r"\b[čc]\S+\s+bud[ěe]jovice\b",
            {
                "place": "České Budějovice",
                "region": "České Budějovice",
                "country": "Česko",
            },
        ),
        (r"^česko$", None),
        (r"^czechia$", None),
        (r"^česká rep[a-z\.]+$", None),
        (r"^czech rep[a-z\.]+$", None),
    ]
]

REGIONS_MAPPING = {
    # countries
    "Deutschland": "Německo",
    "Polska": "Polsko",
    "Österreich": "Rakousko",
    # regions
    "Hlavní město Praha": "Praha",
    "Středočeský kraj": "Praha",
    "Jihočeský kraj": "České Budějovice",
    "Plzeňský kraj": "Plzeň",
    "Karlovarský kraj": "Karlovy Vary",
    "Ústecký kraj": "Ústí nad Labem",
    "Liberecký kraj": "Liberec",
    "Královéhradecký kraj": "Hradec Králové",
    "Pardubický kraj": "Pardubice",
    "Olomoucký kraj": "Olomouc",
    "Moravskoslezský kraj": "Ostrava",
    "Jihomoravský kraj": "Brno",
    "Zlínský kraj": "Zlín",
    "Kraj Vysočina": "Jihlava",
}

ADDRESS_TYPES_MAPPING = {
    # Mapy.cz
    "muni": "place",
    "regi": "region",
    "coun": "country",
    # OpenStreetMaps
    "osmm": "place",
    "osmr": "region",
    "osmc": "country",
}

RETRY_ON_503_MAX_SECONDS = 3


class GeocodeError(Exception):
    pass


def fetch_locations(locations_raw, **kwargs):
    parse_results = [
        fetch_location(location_raw, **kwargs) for location_raw in locations_raw
    ]
    parse_results = set(filter(None, parse_results))
    return [dict(name=name, region=region) for name, region in parse_results]


def fetch_location(location_raw, geocode=None, debug_info=None):
    geocode = geocode or geocode_mapycz
    try:
        logger.debug(f"Geocoding '{location_raw}'")
        address = geocode(location_raw)
        if address:
            try:
                return (address["place"], get_region(address))
            except KeyError as e:
                raise KeyError(f"{address!r} doesn't have key {e}") from e
    except Exception:
        debug_suffix = f", {debug_info!r}" if debug_info else ""
        logger.exception(f"Geocoding '{location_raw}' failed{debug_suffix}")


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
        logger.debug(f"Geocoding '{location_raw}' using api.mapy.cz/v0/geocode")
        response = requests.get(
            "https://api.mapy.cz/v0/geocode",
            params={"query": location_raw},
            headers=MAPYCZ_REQUEST_HEADERS,
            timeout=MAPYCZ_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        xml = etree.fromstring(response.content)
        items = xml.xpath("//item")
        if not items:
            logger.debug(f"Geocoding '{location_raw}' resulted in nothing")
            return None

        item = items[0]
        title, lat, lng = item.get("title"), item.get("y"), item.get("x")
    except requests.RequestException as e:
        raise GeocodeError(f"Unable to geocode '{location_raw}'") from e

    try:
        logger.debug(
            f"Reverse geocoding '{location_raw}' lat: {lat} lng: {lng} using api.mapy.cz/v0/rgeocode"
        )
        response = requests.get(
            "https://api.mapy.cz/v0/rgeocode",
            params={"lat": lat, "lon": lng},
            headers=MAPYCZ_REQUEST_HEADERS,
            timeout=MAPYCZ_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        xml = etree.fromstring(response.content)
        items = xml.xpath("//item")
        if not items:
            raise ValueError("No items in the reverse geocode response")

        logger.debug(
            f"Reverse geocoding '{location_raw}' lat: {lat} lng: {lng} resulted in {item.attrib!r}"
        )
        address = {
            ADDRESS_TYPES_MAPPING[item.attrib["type"]]: item.attrib["name"]
            for item in items
            if item.attrib["type"] in ADDRESS_TYPES_MAPPING
        }
        return address
    except requests.RequestException as e:
        raise GeocodeError(
            f"Unable to geocode '{location_raw}' (unable to reverse geocode '{title}' lat: {lat} lng: {lng})"
        ) from e


def get_region(address):
    if address["country"].lower().startswith("česk"):
        region = address["region"]
    else:
        region = address["country"]
    return REGIONS_MAPPING.get(region, region)


if __name__ == "__main__":
    """
    Usage:

        poetry run python -m juniorguru.lib.locations 'Ústí nad Orlicí, Pardubice, Czechia'
    """
    import sys
    from pprint import pprint

    location_raw = sys.argv[1]
    print("geocode_mapycz()")
    pprint(geocode_mapycz(location_raw))
    print("---\nfetch_locations()")
    pprint(fetch_locations([location_raw]))
