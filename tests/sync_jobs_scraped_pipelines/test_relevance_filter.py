import pytest

from jg.coop.sync.jobs_scraped import DropItem
from jg.coop.sync.jobs_scraped.pipelines.relevance_filter import process


@pytest.mark.parametrize(
    "item",
    [
        dict(llm_opinion=dict(is_sw_engineering=True)),
        dict(llm_opinion=dict(is_sw_engineering=True, is_sw_testing=False)),
        dict(llm_opinion=dict(is_sw_engineering=True, is_sw_testing=True)),
        dict(llm_opinion=dict(is_sw_engineering=False, is_sw_testing=True)),
        dict(llm_opinion=dict(is_sw_testing=True)),
    ],
)
@pytest.mark.asyncio
async def test_relevance_filter(item: dict):
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
            "Not relevant: missing opinion on SW engineering, missing opinion on SW testing",
        ),
        (
            dict(llm_opinion=dict(is_sw_engineering=False)),
            "Not relevant: not SW engineering, missing opinion on SW testing",
        ),
        (
            dict(llm_opinion=dict(is_sw_testing=False)),
            "Not relevant: missing opinion on SW engineering, not SW testing",
        ),
        (
            dict(llm_opinion=dict(is_sw_engineering=False, is_sw_testing=False)),
            "Not relevant: not SW engineering, not SW testing",
        ),
    ],
)
@pytest.mark.asyncio
async def test_relevance_filter_drops(item: dict, message: str):
    with pytest.raises(DropItem, match=message):
        await process(item)
