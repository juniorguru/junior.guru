import pytest

from jg.coop.lib.location import (
    Location,
    ResponseCountry,
    ResponseRegion,
    ResponseRegionType,
    get_region_name,
    repr_locations,
)


@pytest.mark.parametrize(
    "country, regions, expected",
    [
        (
            ResponseCountry(
                name="Slovensko", type=ResponseRegionType.country, isoCode="SK"
            ),
            [
                ResponseRegion(name="Okres Pezinok", type=ResponseRegionType.region),
                ResponseRegion(
                    name="Bratislavský kraj", type=ResponseRegionType.region
                ),
            ],
            "Bratislava",
        ),
    ],
)
def test_get_region_name(country, regions, expected):
    assert get_region_name(country, regions) == expected


@pytest.mark.parametrize(
    "locations, remote, expected",
    [
        (
            [],
            False,
            "kdekoliv",
        ),
        (
            [],
            True,
            "na dálku",
        ),
        (
            [
                Location(
                    raw="Ústí nad Orlicí, Pardubice, Czechia",
                    place="Ústí nad Orlicí",
                    region="Pardubice",
                    country_code="CZ",
                ),
            ],
            False,
            "Ústí nad Orlicí (Pardubice)",
        ),
        (
            [
                Location(
                    raw="Bratislava, Bratislava, Slovakia",
                    place="Bratislava",
                    region="Bratislava",
                    country_code="SK",
                ),
            ],
            False,
            "Bratislava",
        ),
        (
            [
                Location(
                    raw="Ústí nad Orlicí, Pardubice, Czechia",
                    place="Ústí nad Orlicí",
                    region="Pardubice",
                    country_code="CZ",
                ),
            ],
            True,
            "Ústí nad Orlicí (Pardubice), na dálku",
        ),
        (
            [
                Location(
                    raw="Bratislava, Bratislava, Slovakia",
                    place="Bratislava",
                    region="Bratislava",
                    country_code="SK",
                ),
            ],
            True,
            "Bratislava, na dálku",
        ),
        (
            [
                Location(
                    raw="Ústí nad Orlicí, Pardubice, Czechia",
                    place="Ústí nad Orlicí",
                    region="Pardubice",
                    country_code="CZ",
                ),
                Location(
                    raw="Bratislava, Bratislava, Slovakia",
                    place="Bratislava",
                    region="Bratislava",
                    country_code="SK",
                ),
            ],
            False,
            "Bratislava, Ústí nad Orlicí (Pardubice)",
        ),
        (
            [
                Location(
                    raw="Ústí nad Orlicí, Pardubice, Czechia",
                    place="Ústí nad Orlicí",
                    region="Pardubice",
                    country_code="CZ",
                ),
                Location(
                    raw="Bratislava, Bratislava, Slovakia",
                    place="Bratislava",
                    region="Bratislava",
                    country_code="SK",
                ),
                Location(
                    raw="Brno, Jihomoravský kraj, Czechia",
                    place="Brno",
                    region="Brno",
                    country_code="CZ",
                ),
                Location(
                    raw="Košice, Košický kraj, Slovakia",
                    place="Košice",
                    region="Košice",
                    country_code="SK",
                ),
            ],
            False,
            "Bratislava, Brno a další",
        ),
        (
            [
                Location(
                    raw="Ústí nad Orlicí, Pardubice, Czechia",
                    place="Ústí nad Orlicí",
                    region="Pardubice",
                    country_code="CZ",
                ),
                Location(
                    raw="Bratislava, Bratislava, Slovakia",
                    place="Bratislava",
                    region="Bratislava",
                    country_code="SK",
                ),
                Location(
                    raw="Brno, Jihomoravský kraj, Czechia",
                    place="Brno",
                    region="Brno",
                    country_code="CZ",
                ),
                Location(
                    raw="Košice, Košický kraj, Slovakia",
                    place="Košice",
                    region="Košice",
                    country_code="SK",
                ),
            ],
            True,
            "Bratislava, Brno a další, na dálku",
        ),
        (
            [
                Location(
                    raw="Praha – Stodůlky",
                    place="Praha",
                    region="Praha",
                    country_code="CZ",
                ),
                Location(
                    raw="Siemensova 2715/1, Praha – Stodůlky",
                    place="Praha",
                    region="Praha",
                    country_code="CZ",
                ),
            ],
            False,
            "Praha",
        ),
    ],
)
def test_repr_locations(locations, remote, expected):
    assert repr_locations(locations, remote) == expected
