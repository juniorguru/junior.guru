import pytest

from jg.coop.sync.jobs_scraped.pipelines.canonical_url import process


@pytest.mark.parametrize(
    "item, expected",
    [
        pytest.param(
            dict(
                url="https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate"
            ),
            dict(
                canonical_ids=["startupjobs#48407/venture-capital-analyst-associate"],
                url="https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
                source_urls=[
                    "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate"
                ],
            ),
            id="single URL",
        ),
        pytest.param(
            dict(
                url="https://www.linkedin.com/jobs/view/4334211481",
                apply_url="https://mafra.jobs.cz/detail-pozice?r=detail&id=2000805294",
                source_urls=[
                    "https://www.linkedin.com/jobs/search?keywords=junior%20programator&location=Czechia&geoId=104508036&f_TPR=r86400&position=1&pageNum=0"
                ],
            ),
            dict(
                canonical_ids=["jobscz#2000805294", "linkedin#4334211481"],
                url="https://www.jobs.cz/rpd/2000805294/",
                apply_url="https://mafra.jobs.cz/detail-pozice?r=detail&id=2000805294",
                source_urls=[
                    "https://www.linkedin.com/jobs/search?keywords=junior%20programator&location=Czechia&geoId=104508036&f_TPR=r86400&position=1&pageNum=0",
                    "https://www.linkedin.com/jobs/view/4334211481",
                ],
            ),
            id="multiple source URLs and IDs",
        ),
        pytest.param(
            dict(
                url="https://www.linkedin.com/jobs/view/4334211481",
                apply_url="https://mafra.jobs.cz/detail-pozice?r=detail&id=2000805294",
                source_urls=[
                    "https://www.linkedin.com/jobs/search?keywords=junior%20programator&location=Czechia&geoId=104508036&f_TPR=r86400&position=1&pageNum=0",
                    "https://www.linkedin.com/jobs/view/4334211481",
                ],
            ),
            dict(
                canonical_ids=["jobscz#2000805294", "linkedin#4334211481"],
                url="https://www.jobs.cz/rpd/2000805294/",
                apply_url="https://mafra.jobs.cz/detail-pozice?r=detail&id=2000805294",
                source_urls=[
                    "https://www.linkedin.com/jobs/search?keywords=junior%20programator&location=Czechia&geoId=104508036&f_TPR=r86400&position=1&pageNum=0",
                    "https://www.linkedin.com/jobs/view/4334211481",
                ],
            ),
            id="deduplicate source URLs",
        ),
    ],
)
@pytest.mark.asyncio
async def test_canonical_url(item: dict, expected: dict):
    item = await process(item)

    assert item == expected


@pytest.mark.asyncio
async def test_canonical_url_without_url():
    with pytest.raises(RuntimeError, match="Item has no URL"):
        await process({})


@pytest.mark.asyncio
async def test_canonical_url_no_ids():
    item = {
        "url": "https://example.com/",
        "apply_url": "https://example.com/apply",
        "source_urls": [],
    }

    with pytest.raises(NotImplementedError, match="Could not parse canonical IDs"):
        await process(item)
