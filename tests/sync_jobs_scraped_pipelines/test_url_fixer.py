import pytest

from jg.coop.sync.jobs_scraped.pipelines.url_fixer import fix_url, process


@pytest.mark.asyncio
async def test_url_fixer():
    item = await process(
        {
            "url": "example.com",
            "apply_url": "example.com/apply",
            "company_url": "example.com/company",
            "company_logo_urls": ["example.com/logo.png", "example.com/logo2.png"],
            "source_urls": ["example.com/source"],
        }
    )

    assert item == {
        "url": "https://example.com",
        "apply_url": "https://example.com/apply",
        "company_url": "https://example.com/company",
        "company_logo_urls": [
            "https://example.com/logo.png",
            "https://example.com/logo2.png",
        ],
        "source_urls": ["https://example.com/source"],
    }


@pytest.mark.parametrize(
    "url, expected",
    [("example.com", "https://example.com"), ("", None), (None, None)],
)
def test_fix_url(url, expected):
    assert fix_url(url) == expected
