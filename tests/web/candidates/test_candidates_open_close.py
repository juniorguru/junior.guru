import re

import pytest
from playwright.sync_api import Page, TimeoutError, expect
from web.helpers import create_candidate, create_candidate_project


def test_candidates_are_closed_initially(page: Page, candidates_page):
    candidate = create_candidate(name="Ada Lovelace", email="ada@example.com")
    create_candidate_project(candidate)
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    expect(item).not_to_have_class(re.compile(r"\bopen\b"))
    expect(item.locator(".candidates-title-link")).to_be_visible()
    expect(item.locator(".candidates-open")).to_be_visible()
    expect(item.locator(".candidates-close")).to_be_hidden()
    expect(item.locator(".candidates-actions")).to_be_hidden()
    expect(item.locator(".candidates-projects")).to_be_hidden()
    expect(item.locator(".candidates-details")).to_be_hidden()
    expect(item.locator(".candidates-action-email")).to_be_hidden()


def test_clicking_title_opens_candidate(page: Page, candidates_page):
    candidate = create_candidate(name="Ada Lovelace", email="ada@example.com")
    create_candidate_project(candidate)
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()

    expect(page).to_have_url(re.compile(r"/candidates/$"))
    assert len(page.context.pages) == 1
    expect(item).to_have_class(re.compile(r"\bopen\b"))
    expect(item.locator(".candidates-title-link")).to_be_hidden()
    expect(item.locator(".candidates-open")).to_be_hidden()
    expect(item.locator(".candidates-title-text")).to_be_visible()
    expect(item.locator(".candidates-title-text")).to_have_text("Ada Lovelace")
    expect(item.locator(".candidates-close")).to_be_visible()
    expect(item.locator(".candidates-actions")).to_be_visible()
    expect(item.locator(".candidates-projects")).to_be_visible()
    expect(item.locator(".candidates-details")).to_be_visible()


def test_clicking_close_closes_candidate(page: Page, candidates_page):
    candidate = create_candidate(name="Ada Lovelace", email="ada@example.com")
    create_candidate_project(candidate)
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()
    item.locator(".candidates-close").click()

    expect(item).not_to_have_class(re.compile(r"\bopen\b"))
    expect(item.locator(".candidates-title-link")).to_be_visible()
    expect(item.locator(".candidates-open")).to_be_visible()
    expect(item.locator(".candidates-title-text")).to_be_hidden()
    expect(item.locator(".candidates-close")).to_be_hidden()
    expect(item.locator(".candidates-actions")).to_be_hidden()
    expect(item.locator(".candidates-projects")).to_be_hidden()
    expect(item.locator(".candidates-details")).to_be_hidden()
    expect(item.locator(".candidates-action-email")).to_be_hidden()


def test_opening_one_candidate_leaves_others_closed(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace")
    create_candidate(name="Grace Hopper")
    candidates_page()
    page.goto("/candidates/")

    ada = page.locator(".candidates-item.tagged", has_text="Ada Lovelace")
    grace = page.locator(".candidates-item.tagged", has_text="Grace Hopper")
    ada.locator(".candidates-title-link").click()

    expect(ada).to_have_class(re.compile(r"\bopen\b"))
    expect(grace).not_to_have_class(re.compile(r"\bopen\b"))
    expect(grace.locator(".candidates-actions")).to_be_hidden()


def test_clicking_anywhere_on_candidate_opens_it(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", regions=["Brno"])
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    location = item.locator(".candidates-info").get_by_text("Brno")
    box = location.bounding_box()
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)

    expect(item).to_have_class(re.compile(r"\bopen\b"))
    expect(page).to_have_url(re.compile(r"/candidates/$"))


def test_title_links_to_github(page: Page, candidates_page):
    """
    Regression: the title used to link to e-mail or LinkedIn, if available
    """
    create_candidate(
        name="Ada Lovelace",
        github_username="ada",
        email="ada@example.com",
        linkedin_url="https://www.linkedin.com/in/ada/",
    )
    candidates_page()
    page.goto("/candidates/")

    expect(page.locator(".candidates-title-link")).to_have_attribute(
        "href", "https://github.com/ada"
    )


@pytest.mark.parametrize(
    "linkedin_url, email, buttons, hrefs",
    [
        (
            None,
            None,
            ["GitHub"],
            ["https://github.com/ada"],
        ),
        (
            "https://www.linkedin.com/in/ada/",
            None,
            ["GitHub", "LinkedIn"],
            ["https://github.com/ada", "https://www.linkedin.com/in/ada/"],
        ),
        pytest.param(
            None,
            "ada@example.com",
            ["GitHub", "E-mail"],
            ["https://github.com/ada", "mailto:ada@example.com"],
            marks=pytest.mark.xfail(
                reason=(
                    "Bug: without LinkedIn, the GitHub button is styled "
                    "as the main contact, even if there's e-mail"
                ),
                strict=True,
                raises=AssertionError,
            ),
        ),
        (
            "https://www.linkedin.com/in/ada/",
            "ada@example.com",
            ["GitHub", "LinkedIn", "E-mail"],
            [
                "https://github.com/ada",
                "https://www.linkedin.com/in/ada/",
                "mailto:ada@example.com",
            ],
        ),
    ],
)
def test_contact_buttons(
    page: Page,
    candidates_page,
    linkedin_url: str | None,
    email: str | None,
    buttons: list[str],
    hrefs: list[str],
):
    """
    Regression: the LinkedIn button used to link to the e-mail, if available

    The last button is the main contact, the others are profile links.
    """
    create_candidate(
        name="Ada Lovelace",
        github_username="ada",
        linkedin_url=linkedin_url,
        email=email,
    )
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()
    actions = item.locator(".candidates-action-button")
    expect(actions).to_have_text(buttons)
    assert [a.get_attribute("href") for a in actions.all()] == hrefs
    expect(actions.last).to_have_class(re.compile(r"\bcontact\b"))
    for action in actions.all()[:-1]:
        expect(action).to_have_class(re.compile(r"\bprofile\b"))


def test_email_is_shown_only_when_open(page: Page, candidates_page):
    """
    Regression: the e-mail address got moved out of the actions, so it needs
    to be revealed on its own when the candidate opens
    """
    create_candidate(name="Ada Lovelace", email="ada@example.com")
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    email = item.locator(".candidates-action-email")
    expect(email).to_be_hidden()
    item.locator(".candidates-title-link").click()

    expect(email).to_be_visible()
    expect(email).to_have_text("ada@example.com")
    expect(item.locator(".candidates-actions-list")).not_to_contain_text(
        "ada@example.com"
    )


def test_email_is_obfuscated(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", email="ada@example.com")
    candidates_page()
    page.goto("/candidates/")

    html = page.locator(".candidates-action-email").inner_html()
    assert "ada@example.com" not in html


def test_candidate_without_email_has_no_email_box(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace")
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()
    expect(item.locator(".candidates-action-email")).to_have_count(0)


@pytest.mark.parametrize(
    "selector",
    [
        ".candidates-action-button",
        ".candidates-project-link",
        ".candidates-details a",
    ],
)
def test_open_candidate_links_are_clickable(page: Page, candidates_page, selector: str):
    candidate = create_candidate(
        name="Ada Lovelace",
        is_ready=False,
        report_url="https://github.com/juniorguru/eggtray/issues/42",
    )
    create_candidate_project(candidate, demo_url="https://example.com/demo")
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()
    link = item.locator(selector).first
    href = link.get_attribute("href")
    requested_urls = []
    page.context.on("request", lambda request: requested_urls.append(request.url))
    with page.context.expect_page() as new_page_info:
        link.click()

    assert new_page_info.value.opener() == page
    assert href in requested_urls
    expect(item).to_have_class(re.compile(r"\bopen\b"))


def test_open_candidate_badges_show_tooltips(page: Page, candidates_page):
    candidate = create_candidate(name="Ada Lovelace", university="it")
    create_candidate_project(candidate)
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()
    item.locator(".candidates-badge", has_text="IT VŠ").hover()

    tooltip = page.locator(".tooltip.candidates-badge-tooltip")
    expect(tooltip).to_be_visible()
    expect(tooltip).to_have_text("Má vystudovanou IT VŠ")


@pytest.mark.xfail(
    reason="Bug: clicks with a modifier key open the candidate instead of a new tab",
    strict=True,
    raises=(AssertionError, TimeoutError),
)
def test_modifier_click_on_title_opens_new_tab(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", github_username="ada")
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    requested_urls = []
    page.context.on("request", lambda request: requested_urls.append(request.url))
    with page.context.expect_page(timeout=2_000) as new_page_info:
        item.locator(".candidates-title-link").click(modifiers=["ControlOrMeta"])

    assert new_page_info.value.opener() == page
    assert "https://github.com/ada" in requested_urls
    expect(item).not_to_have_class(re.compile(r"\bopen\b"))
    expect(item.locator(".candidates-actions")).to_be_hidden()
