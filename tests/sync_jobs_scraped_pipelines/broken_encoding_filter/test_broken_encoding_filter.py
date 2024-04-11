from pathlib import Path

import pytest

from jg.coop.sync.jobs_scraped import DropItem
from jg.coop.sync.jobs_scraped.pipelines.broken_encoding_filter import process


fixtures_raising = [
    pytest.param(path.read_text(), id=path.name)
    for path in (Path(__file__).parent).rglob("*.html")
    if path.name.startswith("raising")
]
assert len(fixtures_raising) > 0, "No fixtures found"


@pytest.mark.parametrize("description_html", fixtures_raising)
@pytest.mark.asyncio
async def test_broken_encoding_filter_raising(description_html: str):
    with pytest.raises(DropItem):
        await process(dict(description_html=description_html))


fixtures_passing = [
    pytest.param(path.read_text(), id=path.name)
    for path in (Path(__file__).parent).rglob("*.html")
    if path.name.startswith("passing")
]
assert len(fixtures_passing) > 0, "No fixtures found"


@pytest.mark.parametrize("description_html", fixtures_passing)
@pytest.mark.asyncio
async def test_broken_encoding_filter_passing(description_html: str):
    await process(dict(description_html=description_html))
