import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_job


LONG_TITLE = (
    "Junior Python Developer for Backend Development of Internal Systems "
    "with Occasional Frontend Work and Mentoring"
)


def test_close_button_stays_at_top_of_wrapped_title(page: Page, jobs_page):
    """
    Regression: the close button used to be misaligned when the title wrapped,
    see https://github.com/juniorguru/junior.guru/issues/1751
    """
    create_job(title=LONG_TITLE)
    jobs_page()
    page.set_viewport_size({"width": 600, "height": 800})
    page.goto("/jobs/")

    job = page.locator(".jobs-item.tagged")
    job.locator(".jobs-title-link").click()

    title = job.locator(".jobs-title-text").bounding_box()
    close = job.locator(".jobs-close").bounding_box()
    assert title["height"] > close["height"] * 2, "title should wrap"
    assert abs(close["y"] - title["y"]) < 8


def test_region_tag_is_not_stretched(page: Page, jobs_page):
    """
    Regression: the link to all regions used to stretch the region tag
    """
    create_job(title="Brno Developer", regions=["Brno"], employment_types=["fulltime"])
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/")

    region_tag = page.locator(".jobs-filters [data-jobs-tag='brno']")
    expect(region_tag).to_be_visible()
    employment_tag = page.locator(".jobs-filters [data-jobs-tag='fulltime']")
    region_box = region_tag.bounding_box()
    employment_box = employment_tag.bounding_box()
    assert abs(region_box["height"] - employment_box["height"]) < 1


@pytest.mark.parametrize(
    "context_options",
    [{"viewport": {"width": 360, "height": 800}, "is_mobile": True}],
)
@pytest.mark.parametrize("url", ["/jobs/", "/jobs/brno/"])
def test_no_horizontal_scroll_on_mobile(page: Page, jobs_page, url: str):
    create_job(
        title=LONG_TITLE,
        regions=["Brno"],
        remote=True,
        employment_types=["fulltime", "parttime", "internship"],
        tech_tags=["python", "javascript", "typescript", "kubernetes", "postgresql"],
        canonical_ids=["linkedin#1", "startupjobs#1"],
        company_url="https://example.com",
    )
    jobs_page(url)
    page.goto(url)
    page.locator(".jobs-item.tagged .jobs-title-link").click()

    scroll_width = page.evaluate("document.documentElement.scrollWidth")
    assert scroll_width <= 360
