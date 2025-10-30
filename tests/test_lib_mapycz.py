import pytest

from jg.coop.lib.mapycz import (
    ResponseCountry,
    ResponseRegion,
    ResponseRegionType,
    get_region_name,
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
