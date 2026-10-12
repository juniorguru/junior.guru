import pytest

from jg.coop.lib.location import Location
from jg.coop.sync import jobs_locations
from jg.coop.sync.jobs_locations import LocationsList, is_relevant, locate_list


async def fake_locate(location_raw: str) -> Location:
    return Location(
        raw=location_raw, place=location_raw, region=location_raw, country_code="SK"
    )


@pytest.fixture
def locate(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(jobs_locations, "locate", fake_locate)


@pytest.mark.asyncio
async def test_locate_list_universal(locate):
    result = await locate_list(["Slovensko", "Bratislava"])

    assert (result.is_universal, [location.raw for location in result.locations]) == (
        True,
        ["Bratislava"],
    )


def make_locations_list(
    country_codes: list[str], is_universal: bool = False
) -> LocationsList:
    return LocationsList(
        locations=[
            Location(raw=code, place=code, region=code, country_code=code)
            for code in country_codes
        ],
        is_universal=is_universal,
    )


@pytest.mark.parametrize(
    "country_codes, is_universal, remote, expected",
    [
        (["CZ"], False, False, True),
        (["DE", "SK"], False, False, True),
        (["DE"], False, False, False),
        ([], False, False, False),
        ([], True, False, True),
        ([], False, True, True),
        (["DE"], False, True, True),
    ],
)
def test_is_relevant(
    country_codes: list[str], is_universal: bool, remote: bool, expected: bool
):
    locations_list = make_locations_list(country_codes, is_universal)

    assert is_relevant(locations_list, remote, {"CZ", "SK"}) is expected
