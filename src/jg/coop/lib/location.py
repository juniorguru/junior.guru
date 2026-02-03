import os
import random
import re
from datetime import timedelta
from decimal import Decimal
from enum import StrEnum
from typing import Generator, Literal

import czech_sort
import httpx
from pydantic import BaseModel

from jg.coop.lib import loggers
from jg.coop.lib.async_utils import limit
from jg.coop.lib.cache import cache
from jg.coop.lib.llm import ask_llm
from jg.coop.lib.mutations import MutationsNotAllowedError


MAPYCZ_API_KEY = os.getenv("MAPYCZ_API_KEY")

DEFAULT_HEADERS = {
    "User-Agent": "JuniorGuruBot (+https://junior.guru)",
}

LANGUAGE_CODE = "cs"

# Includes Czechia and Slovakia (use https://pro.mapy.cz/examples/geocode/ to determine the bounding box)
BOUNDING_BOX = (
    Decimal("11.9343226828355"),
    Decimal("47.642252179452925"),
    Decimal("22.77625295237229"),
    Decimal("51.16150072295437"),
)

REWRITES_RE = {
    re.compile(r"\bSouth Moravia\b", re.I): "Jihomoravský kraj",
    re.compile(r"\bCentral Bohemia\b", re.I): "Středočeský kraj",
    re.compile(r"\bSouth Bohemia\b", re.I): "Jihočeský kraj",
    re.compile(r"\bMoravia-Silesia\b", re.I): "Moravskoslezský kraj",
    re.compile(r"\bMetropolitan Area\b", re.I): "",
    re.compile(r"\(\d+\. patro\)", re.I): "",
    re.compile(r"\bBrno\W+Staré Brno\b", re.I): "Brno",
    re.compile(r"\bPraha\W+Nové Město\b", re.I): "Praha",
    re.compile(r"\bPraha\W+(východ|západ)\b", re.I): "Středočeský kraj",
}

REGIONS_MAPPING_CZ = {
    "kraj Hlavní město Praha": "Praha",
    "Jihočeský kraj": "České Budějovice",
    "Jihomoravský kraj": "Brno",
    "Karlovarský kraj": "Karlovy Vary",
    "Kraj Vysočina": "Jihlava",
    "Královéhradecký kraj": "Hradec Králové",
    "Liberecký kraj": "Liberec",
    "Moravskoslezský kraj": "Ostrava",
    "Olomoucký kraj": "Olomouc",
    "Pardubický kraj": "Pardubice",
    "Plzeňský kraj": "Plzeň",
    "Středočeský kraj": "Praha",
    "Ústecký kraj": "Ústí nad Labem",
    "Zlínský kraj": "Zlín",
}

REGIONS_MAPPING_SK = {
    "Banskobystrický kraj": "Banská Bystrica",
    "Bratislavský kraj": "Bratislava",
    "Košický kraj": "Košice",
    "Nitranský kraj": "Nitra",
    "Prešovský kraj": "Prešov",
    "Trenčínský kraj": "Trenčín",
    "Trnavský kraj": "Trnava",
    "Žilinský kraj": "Žilina",
}

REGIONS = sorted(
    set(REGIONS_MAPPING_CZ.values()) | set(REGIONS_MAPPING_SK.values()),
    key=czech_sort.key,
)

ZIP_CODE_RE = re.compile(r"\b\d{3} ?\d{2}\b")


class Location(BaseModel):
    raw: str
    place: str
    region: str
    country_code: str


class LLMFuzzyLocation(BaseModel):
    locations: list[str]
    is_universal: bool


class FuzzyLocation(BaseModel):
    locations: list[Location]
    is_universal: bool


class ResponseRegionType(StrEnum):
    address = "regional.address"
    street = "regional.street"
    municipality_part = "regional.municipality_part"
    municipality = "regional.municipality"
    region = "regional.region"
    country = "regional.country"


class ResponseRegion(BaseModel):
    name: str  # e.g. 'okres Ústí nad Orlicí' or 'Pardubický kraj'
    type: ResponseRegionType


class ResponseCountry(BaseModel):
    name: str  # e.g. 'Česko'
    type: Literal[ResponseRegionType.country]
    isoCode: str  # e.g. 'CZ'


class ResponseCoords(BaseModel):
    lon: Decimal  # e.g. 16.39361
    lat: Decimal  # e.g. 49.97387


class ResponseItem(BaseModel):
    name: str  # e.g. 'Ústí nad Orlicí'
    label: str  # e.g. 'Město'
    position: ResponseCoords
    type: ResponseRegionType
    location: str  # e.g. 'Česko'
    regionalStructure: list[ResponseRegion | ResponseCountry]


logger = loggers.from_path(__file__)


async def locate_fuzzy(location_raw: str) -> Location:
    try:
        fuzzy_location: LLMFuzzyLocation = await ask_llm(
            """
                You are an assistant who helps to identify locations based on user input.
                Sometimes the user input may refer to multiple locations or be ambiguous.
                Analyze the given location input and provide:

                - A list of locations if the input tries to refer to multiple places.
                If the input is clear and refers to a single location,
                provide a list with just that one location.

                Example: For the input "Prague, Brno - Czechia", return ["Prague, Czechia", "Brno, Czechia"]
                Example: For the input "Ostrava", return ["Ostrava"]

                - A boolean indicating whether the user tries to refer to a universal
                location (e.g., "Czechia", "Slovakia", "remote", "anywhere").

                Example: For the input "Czechia", return true
                Example: For the input "Slovakia", return true
                Example: For the input "Brno", return false
                Example: For the input "Praha, Brno, Ostrava (remote)", return true
                Example: For the input "Europe", return true

                The context of processing the input is Czechia and Slovakia.
            """,
            location_raw,
            schema=LLMFuzzyLocation,
        )
        return FuzzyLocation(
            locations=[
                await locate(raw_location) for raw_location in fuzzy_location.locations
            ],
            is_universal=fuzzy_location.is_universal,
        )
    except MutationsNotAllowedError:
        logger.warning("Generating random fuzzy location")
        return FuzzyLocation(
            locations=[await locate(location_raw)],
            is_universal=random.choice([True, False, False, False, False]),
        )


@cache(
    expire=timedelta(days=60), tag="location-locate", ignore=("api_key", "bounding_box")
)
async def locate(
    location_raw: str,
    api_key: str | None = None,
    bounding_box: tuple[Decimal, Decimal, Decimal, Decimal] | None = None,
) -> Location:
    api_key = api_key or MAPYCZ_API_KEY
    bounding_box = bounding_box or BOUNDING_BOX

    async with limit(4):
        logger.debug(f"Locating: {location_raw!r}")
        async with httpx.AsyncClient(headers=DEFAULT_HEADERS) as client:
            for query, type in generate_queries(location_raw):
                logger.debug(f"Locating as {type}: {query!r}")
                # See also https://pro.mapy.cz/examples/geocode/
                response = await client.get(
                    "https://api.mapy.cz/v1/geocode",
                    params={
                        "apikey": api_key,
                        "query": query,
                        "lang": LANGUAGE_CODE,
                        "type": type,
                        "preferBBox": ",".join(map(str, BOUNDING_BOX)),
                    },
                )
                response.raise_for_status()

                if items := response.json()["items"]:
                    item = ResponseItem(**items[0])
                    logger.debug(f"Processing: {item!r}")
                    location = get_location(location_raw, item)
                    logger.debug(f"Located! {location.model_dump()!r}")
                    return location

    raise ValueError(f"Unable to locate: {location_raw!r}")


def generate_queries(
    location_raw: str,
) -> Generator[tuple[str, ResponseRegionType], None, None]:
    # rewrite strings not recognized by the API
    for rewrite_re, rewrite_value in REWRITES_RE.items():
        location_raw = rewrite_re.sub(rewrite_value, location_raw)
    location_raw = ", ".join(filter(None, map(str.strip, location_raw.split(","))))

    # if contains a comma and number
    if "," in location_raw and re.search(r"\d", location_raw):
        yield location_raw, ResponseRegionType.address

    yield location_raw, ResponseRegionType.municipality
    yield location_raw, ResponseRegionType.municipality_part
    yield location_raw, ResponseRegionType.region
    yield location_raw, ResponseRegionType.country

    # if contains a number
    if re.search(r"\d", location_raw):
        yield location_raw, ResponseRegionType.address

    # remove zip code if present
    if ZIP_CODE_RE.search(location_raw):
        location_raw = ZIP_CODE_RE.sub("", location_raw)
        yield from generate_queries(location_raw)

    # remove the first part (e.g. TietoEvry Organica Ostrava, Nám. Biskupa Bruna 3399/5, Ostrava)
    if "," in location_raw:
        _, location_raw = location_raw.split(",", 1)
        yield from generate_queries(location_raw)


def get_location(location_raw: str, item: ResponseItem) -> Location:
    municipalities = [
        admin_unit
        for admin_unit in item.regionalStructure
        if admin_unit.type == ResponseRegionType.municipality
    ]
    municipality_name = municipalities[-1].name if municipalities else None

    country = [
        admin_unit
        for admin_unit in item.regionalStructure
        if admin_unit.type == ResponseRegionType.country
    ][-1]
    regions = [
        admin_unit
        for admin_unit in item.regionalStructure
        if admin_unit.type == ResponseRegionType.region
    ]
    try:
        region_name = get_region_name(country, regions)
    except:
        logger.error(f"Unable to get region name for {country!r}, {regions!r}")
        raise

    return Location(
        raw=location_raw,
        place=municipality_name or region_name,
        region=region_name,
        country_code=country.isoCode,
    )


def get_region_name(country: ResponseCountry, regions: list[ResponseRegion]) -> str:
    if country.isoCode == "CZ":
        if not regions:
            return "Česko"
        region_name_official = regions[-1].name
        return REGIONS_MAPPING_CZ[region_name_official]

    if country.isoCode == "SK":
        if not regions:
            return "Slovensko"
        try:
            if regions[-1].name == "Bratislavský kraj":
                return "Bratislava"
            # avoiding e.g. 'oblast RŠÚJ Západné Slovensko'
            region_name_official = regions[-2].name
        except IndexError:
            return "Bratislava"
        if "Bratislava" in region_name_official:
            # stuff like 'Okres Bratislava III'
            return "Bratislava"
        return REGIONS_MAPPING_SK[region_name_official]

    return country.name


def repr_locations(locations: list[Location], remote: bool = False) -> str | None:
    if not locations:
        return "na dálku" if remote else None

    places = set()
    for location in locations:
        if location.region and location.place != location.region:
            place = f"{location.place} ({location.region})"
        else:
            place = location.place
        places.add(place)
    places = sorted(places, key=czech_sort.key)

    if len(places) == 1:
        result = places[0]
    elif len(places) == 2:
        result = ", ".join(places)
    else:
        top_two = places[:2]
        result = f"{top_two[0]}, {top_two[1]} a další"
    if remote:
        result = f"{result}, na dálku"

    return result
