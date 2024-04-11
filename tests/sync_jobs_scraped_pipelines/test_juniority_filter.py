import pytest

from jg.coop.sync.jobs_scraped import DropItem
from jg.coop.sync.jobs_scraped.pipelines.juniority_filter import process


@pytest.mark.parametrize(
    "item",
    [
        dict(llm_opinion=dict(is_entry_level=True)),
        dict(llm_opinion=dict(is_entry_level=True, reason="Blah blah blah.")),
    ],
)
@pytest.mark.asyncio
async def test_juniority_filter(item: dict):
    await process(item)


@pytest.mark.parametrize(
    "item, message",
    [
        (
            dict(),
            "Missing LLM opinion",
        ),
        (
            dict(llm_opinion=dict()),
            "Missing LLM opinion",
        ),
        (
            dict(llm_opinion=dict(is_purple=True)),
            "Not for juniors: missing opinion",
        ),
        (
            dict(llm_opinion=dict(is_entry_level=False)),
            "Not for juniors: missing reason",
        ),
        (
            dict(llm_opinion=dict(is_entry_level=False, reason="Blah blah blah.")),
            "Not for juniors: Blah blah blah.",
        ),
    ],
)
@pytest.mark.asyncio
async def test_juniority_filter_drops(item: dict, message: str):
    with pytest.raises(DropItem, match=message):
        await process(item)
