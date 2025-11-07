import pytest

from jg.coop.sync.jobs_scraped.pipelines.utm_params import process


@pytest.mark.parametrize(
    "item, expected",
    [
        pytest.param(
            dict(
                url="https://www.startupjobs.cz/nabidka/97145/backend-engineer",
            ),
            "https://www.startupjobs.cz/nabidka/97145/backend-engineer?utm_source=juniorguru",
            id="No UTM params",
        ),
        pytest.param(
            dict(
                url="https://www.startupjobs.cz/nabidka/97145/backend-engineer",
                source_urls=[
                    "https://example.com/?utm_source=linkedin&utm_medium=cpc&utm_campaign=linkedin"
                ],
            ),
            "https://www.startupjobs.cz/nabidka/97145/backend-engineer?utm_campaign=linkedin&utm_medium=cpc&utm_source=juniorguru",
            id="Source URL contains params, source changes to JG",
        ),
        pytest.param(
            dict(
                url="https://www.startupjobs.cz/nabidka/97145/backend-engineer",
                apply_url="https://example.com/?utm_source=linkedin&utm_medium=cpc&utm_campaign=linkedin",
            ),
            "https://www.startupjobs.cz/nabidka/97145/backend-engineer?utm_campaign=linkedin&utm_medium=cpc&utm_source=juniorguru",
            id="Apply URL contains params, source changes to JG",
        ),
        pytest.param(
            dict(
                url="https://www.startupjobs.cz/nabidka/97145/backend-engineer",
                apply_url="https://example.com/?utm_source=juniorguru&utm_medium=cpc&utm_campaign=linkedin",
                source_urls=[
                    "https://example.com/?utm_source=juniorguru&utm_medium=web&utm_campaign=linkedin"
                ],
            ),
            "https://www.startupjobs.cz/nabidka/97145/backend-engineer?utm_campaign=linkedin&utm_source=juniorguru",
            id="URLs contain conflicting params, source changes to JG, drop others if differing",
        ),
        pytest.param(
            dict(
                url="https://example.com/?something=12345",
                source_urls=[
                    "https://example.com/?utm_source=linkedin&utm_medium=cpc&utm_campaign=linkedin"
                ],
            ),
            "https://example.com/?something=12345&utm_campaign=linkedin&utm_medium=cpc&utm_source=juniorguru",
            id="Other params in URL are preserved",
        ),
    ],
)
@pytest.mark.asyncio
async def test_utm_params(item: dict, expected: dict):
    item = await process(item)

    assert item["url"] == expected


@pytest.mark.asyncio
async def test_utm_params_without_url():
    with pytest.raises(ValueError, match="Item has no URL"):
        await process({})
