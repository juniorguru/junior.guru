import pytest

from jg.coop.lib.location import Location
from jg.coop.sync import jobs_locations
from jg.coop.sync.jobs_locations import locate_list


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
