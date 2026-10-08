import pytest
from playwright.sync_api import Page
from web.helpers import create_candidate, create_candidate_project


LONG_NAME = (
    "Bartoloměj Maxmilián Svatopluk Křižovnický-Hrabánek z Lichtenštejna "
    "a Nového Města nad Metují"
)


def test_close_button_stays_at_top_of_wrapped_title(page: Page, candidates_page):
    create_candidate(name=LONG_NAME)
    candidates_page()
    page.set_viewport_size({"width": 600, "height": 800})
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()

    title = item.locator(".candidates-title-text").bounding_box()
    close = item.locator(".candidates-close i").bounding_box()
    assert title["height"] > close["height"] * 2, "title should wrap"
    assert abs(close["y"] - title["y"]) < 8


@pytest.mark.parametrize(
    "context_options",
    [{"viewport": {"width": 360, "height": 800}, "is_mobile": True}],
)
def test_no_horizontal_scroll_on_mobile(page: Page, candidates_page):
    candidate = create_candidate(
        name=LONG_NAME,
        regions=["Hradec Králové", "Pardubice"],
        skills=["Python", "JavaScript", "TypeScript", "Kubernetes", "PostgreSQL"],
        languages=["English", "Deutsch", "Français"],
        email="bartolomej.maxmilian.svatopluk@example.com",
        linkedin_url="https://www.linkedin.com/in/bartolomej/",
        university="it",
        secondary_school="it",
        experience=["volunteering", "intern", "trainee", "employee"],
        domains=["finance", "zdravotnictví", "logistika"],
    )
    create_candidate_project(
        candidate,
        title="Velmi dlouhý název projektu, který se nevejde na jeden řádek",
        description="Popis projektu, který je také docela dlouhý a zalomí se",
        demo_url="https://example.com/demo",
    )
    create_candidate_project(candidate)
    candidates_page()
    page.goto("/candidates/")
    page.locator(".candidates-item.tagged .candidates-title-link").click()

    scroll_width = page.evaluate("document.documentElement.scrollWidth")
    assert scroll_width <= 360
