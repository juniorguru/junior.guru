import re

import pytest
from playwright.sync_api import Page, expect

from conftest import create_job


@pytest.mark.parametrize(
    "url, region, tag_slug",
    [
        ("/jobs/brno/", "Brno", "brno"),
        ("/jobs/hradec-kralove/", "Hradec Králové", "hradeckralove"),
    ],
)
def test_region_page_shows_only_jobs_in_region(
    page: Page, jobs_page, url: str, region: str, tag_slug: str
):
    create_job(title="Local Developer", regions=[region])
    create_job(title="Praha Developer", regions=["Praha"])
    create_job(title="Remote Developer", remote=True)
    jobs_page(url)
    page.goto(url)

    region_tag = page.locator(f".jobs-filters [data-jobs-tag='{tag_slug}']")
    expect(region_tag).to_be_visible()
    expect(region_tag).to_have_class(re.compile(r"\bactive\b"))
    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Local Developer")
    expect(page).to_have_url(re.compile(f"{url}$"))


def test_region_page_offers_only_region_and_remote(page: Page, jobs_page):
    create_job(title="Brno Developer", regions=["Brno"])
    create_job(title="Praha Developer", regions=["Praha"])
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/")

    location_tags = page.locator(
        ".jobs-filters [data-jobs-tag-type='location']:visible"
    )
    expect(location_tags).to_have_count(2)
    expect(page.locator(".jobs-filters [data-jobs-tag='praha']")).to_have_count(0)


def test_region_tag_cannot_be_turned_off(page: Page, jobs_page):
    create_job(title="Brno Developer", regions=["Brno"])
    create_job(title="Praha Developer", regions=["Praha"])
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/")

    region_tag = page.locator(".jobs-filters [data-jobs-tag='brno']")
    region_tag.click()

    expect(region_tag).to_have_class(re.compile(r"\bactive\b"))
    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(1)
    expect(page).to_have_url(re.compile(r"/jobs/brno/$"))


def test_region_page_with_remote_shows_both(page: Page, jobs_page):
    create_job(title="Brno Developer", regions=["Brno"])
    create_job(title="Praha Developer", regions=["Praha"])
    create_job(title="Remote Developer", remote=True)
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/")

    page.locator(".jobs-filters [data-jobs-tag='remote']").click()

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(2)
    expect(visible_jobs.filter(has_text="Praha Developer")).to_have_count(0)
    expect(page).to_have_url(re.compile(r"/jobs/brno/\?location=remote$"))


def test_region_page_with_other_filters(page: Page, jobs_page):
    create_job(title="Brno Python", regions=["Brno"], tech_tags=["python"])
    create_job(title="Brno Java", regions=["Brno"], tech_tags=["java"])
    create_job(title="Praha Python", regions=["Praha"], tech_tags=["python"])
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Brno Python")
    expect(page).to_have_url(re.compile(r"/jobs/brno/\?technology=python$"))


def test_region_page_url_restores_filter(page: Page, jobs_page):
    create_job(title="Brno Python", regions=["Brno"], tech_tags=["python"])
    create_job(title="Brno Java", regions=["Brno"], tech_tags=["java"])
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/?technology=java")

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Brno Java")


def test_region_page_empty_state_suggests_remote(page: Page, jobs_page):
    create_job(title="Praha Developer", regions=["Praha"])
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/")

    empty = page.locator(".jobs-empty")
    expect(empty).to_be_visible()
    expect(empty).to_contain_text("#remote")


@pytest.mark.xfail(
    reason=(
        "Bug: the region slug is derived from the URL by removing only the first "
        "hyphen, so on /jobs/usti-nad-labem/ the region tag gets deactivated "
        "and the JS crashes"
    ),
    strict=True,
)
def test_region_page_with_multiword_name(page: Page, jobs_page):
    create_job(title="Ústí Developer", regions=["Ústí nad Labem"])
    create_job(title="Praha Developer", regions=["Praha"])
    jobs_page("/jobs/usti-nad-labem/")
    errors = []
    page.on("pageerror", lambda error: errors.append(error))
    page.goto("/jobs/usti-nad-labem/")

    expect(page.locator(".jobs-filters [data-jobs-tag='ustinadlabem']")).to_have_class(
        re.compile(r"\bactive\b")
    )
    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Ústí Developer")
    expect(page.locator(".jobs-noscript")).to_have_count(0)
    expect(page).to_have_url(re.compile(r"/jobs/usti-nad-labem/$"))
    assert errors == []
