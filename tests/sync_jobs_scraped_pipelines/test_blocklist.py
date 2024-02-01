import pytest
from juniorguru.sync.jobs_scraped import DropItem

from juniorguru.sync.jobs_scraped.pipelines.blocklist import process


@pytest.mark.asyncio
async def test_blocklist_lets_junior_through():
    await process(dict(title="Junior Python Developer"))


@pytest.mark.asyncio
async def test_blocklist_lets_junior_senior_through():
    await process(dict(title="Python Developer, Junior/Senior"))


@pytest.mark.asyncio
async def test_blocklist_lets_senior_junior_through():
    await process(dict(title="Python Developer, Senior/Junior"))


@pytest.mark.asyncio
async def test_blocklist_blocks_senior():
    with pytest.raises(DropItem):
        await process(dict(title="Senior Python Developer"))


@pytest.mark.parametrize(
    "title",
    [
        "PLC Programátor",
        "CNC Programátor",
        "CAM/CAD Programátor",
        "Programátor CNC strojů",
        "Programátor strojů",
        "Programátor(ka) strojů",
    ],
)
@pytest.mark.asyncio
async def test_blocklist_blocks_machine_programmer(title):
    with pytest.raises(DropItem):
        await process(dict(title=title))
