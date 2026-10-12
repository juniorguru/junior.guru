import pytest

from jg.coop.lib.location import (
    Location,
    ResponseCountry,
    ResponseRegion,
    ResponseRegionType,
    generate_queries,
    get_place_names,
    get_region_name,
    is_universal_location,
    repr_locations,
    split_locations,
)


@pytest.mark.parametrize(
    "location_raw, expected",
    [
        (
            "Pikrtova 1737/1A (4. patro), Praha 4",
            (
                "Pikrtova 1737/1A, Praha 4",
                ResponseRegionType.address,
            ),
        ),
        (
            "Bratislava III",
            (
                "Bratislava",
                ResponseRegionType.municipality,
            ),
        ),
        (
            "Hostinec Pod Schody\nHrnčířská 813/23\n602 00 Brno-střed-Veveří ((alias Pivovar Fénix))",
            (
                "Hostinec Pod Schody, Hrnčířská 813/23, 602 00 Brno-Veveří",
                ResponseRegionType.address,
            ),
        ),
        (
            "Greater Hyderabad Area",
            (
                "Hyderabad",
                ResponseRegionType.municipality,
            ),
        ),
        (
            "Národní pavilon Z – Výstaviště České Budějovice, České Budějovice & REUSE festival",
            (
                "České Budějovice",
                ResponseRegionType.municipality,
            ),
        ),
        (
            "Nitriansky kraj",
            (
                "Nitriansky kraj",
                ResponseRegionType.region,
            ),
        ),
        (
            "Kraj Vysočina",
            (
                "Kraj Vysočina",
                ResponseRegionType.region,
            ),
        ),
        (
            "Vysočina",
            (
                "Kraj Vysočina",
                ResponseRegionType.region,
            ),
        ),
        (
            "kraj Vysočina",
            (
                "Kraj Vysočina",
                ResponseRegionType.region,
            ),
        ),
        (
            "Gáň, Trnavský kraj",
            (
                "Gáň, Trnavský kraj",
                ResponseRegionType.municipality,
            ),
        ),
        (
            "Krajská 5, Brno",
            (
                "Krajská 5, Brno",
                ResponseRegionType.address,
            ),
        ),
    ],
)
def test_generate_queries_rewrite(location_raw, expected):
    result = next(generate_queries(location_raw))
    assert result == expected


@pytest.mark.parametrize(
    "country, regions, expected",
    [
        (
            ResponseCountry(
                name="Slovensko",
                type=ResponseRegionType.country,
                isoCode="SK",
            ),
            [
                ResponseRegion(
                    name="Okres Pezinok",
                    type=ResponseRegionType.region,
                ),
                ResponseRegion(
                    name="Bratislavský kraj",
                    type=ResponseRegionType.region,
                ),
            ],
            "Bratislava",
        ),
        (
            ResponseCountry(
                name="Slovensko",
                type=ResponseRegionType.country,
                isoCode="SK",
            ),
            [
                ResponseRegion(
                    name="Okres Žilina",
                    type=ResponseRegionType.region,
                ),
                ResponseRegion(
                    name="Žilinský kraj",
                    type=ResponseRegionType.region,
                ),
            ],
            "Žilina",
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
            None,
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


@pytest.mark.parametrize(
    "location_raw",
    [
        "Slovakia",
        "Slovensko",
        "Slovak Republic",
        "Slovenská republika",
        "Czechia",
        "Česko",
        "Czech Republic",
        "Česká republika",
        " slovensko ",
    ],
)
def test_is_universal_location_country(location_raw):
    assert is_universal_location(location_raw) is True


@pytest.mark.parametrize(
    "location_raw",
    [
        "Bratislava, Slovensko",
        "Bratislavský kraj",
        "okres Vranov nad Topľou",
    ],
)
def test_is_universal_location_place(location_raw):
    assert is_universal_location(location_raw) is False


@pytest.mark.parametrize(
    "location_raw, expected",
    [
        (
            "Prešovský kraj, Košický kraj",
            ["Prešovský kraj", "Košický kraj"],
        ),
        (
            "Jihomoravský kraj, Zlínský kraj, Kraj Vysočina",
            ["Jihomoravský kraj", "Zlínský kraj", "Kraj Vysočina"],
        ),
        (
            "Nitriansky kraj, Trenčiansky kraj",
            ["Nitriansky kraj", "Trenčiansky kraj"],
        ),
        (
            "Bratislavský kraj",
            ["Bratislavský kraj"],
        ),
        (
            "Gáň, Trnavský kraj",
            ["Gáň, Trnavský kraj"],
        ),
        (
            "Bratislava, Bratislavský kraj",
            ["Bratislava, Bratislavský kraj"],
        ),
        (
            "Gáň, Gáň, Galanta",
            ["Gáň, Gáň, Galanta"],
        ),
    ],
)
def test_split_locations(location_raw, expected):
    assert split_locations(location_raw) == expected


@pytest.mark.parametrize(
    "locations_raw, expected",
    [
        (
            ["Bratislava", "Košice"],
            ["Bratislava", "Košice"],
        ),
        (
            ["Prešovský kraj, Košický kraj", "Bratislava"],
            ["Prešovský kraj", "Košický kraj", "Bratislava"],
        ),
        (
            ["Slovensko", "Bratislava", "remote"],
            ["Bratislava"],
        ),
        (
            ["Slovensko"],
            [],
        ),
    ],
)
def test_get_place_names(locations_raw, expected):
    assert get_place_names(locations_raw) == expected
