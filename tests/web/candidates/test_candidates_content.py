import re

import pytest
from playwright.sync_api import Page, TimeoutError, expect
from web.helpers import create_candidate, create_candidate_project


def test_heading(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace")
    candidates_page()
    page.goto("/candidates/")

    expect(page.locator("h1")).to_have_text("Juniorní programátoři a testeři")


def test_intro_is_a_paragraph(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace")
    candidates_page()
    page.goto("/candidates/")

    lead = page.locator(".lead")
    expect(lead.locator("pre, code")).to_have_count(0)
    expect(lead.locator("p").first).to_contain_text("Hledáš do firmy juniora?")


@pytest.mark.parametrize(
    "is_ready, is_member, css_class, other_class",
    [
        (True, True, "highlighted", "muted"),
        (False, True, "muted", "highlighted"),
        (False, False, "muted", "highlighted"),
    ],
)
def test_candidate_is_highlighted_or_muted(
    page: Page,
    candidates_page,
    is_ready: bool,
    is_member: bool,
    css_class: str,
    other_class: str,
):
    create_candidate(name="Ada Lovelace", is_ready=is_ready, is_member=is_member)
    candidates_page()
    page.goto("/candidates/")

    candidate = page.locator(".candidates-item.tagged")
    expect(candidate).to_have_class(re.compile(rf"\b{css_class}\b"))
    expect(candidate).not_to_have_class(re.compile(rf"\b{other_class}\b"))


def test_ready_candidate_who_is_not_member_is_neither_highlighted_nor_muted(
    page: Page, candidates_page
):
    create_candidate(name="Ada Lovelace", is_ready=True, is_member=False)
    candidates_page()
    page.goto("/candidates/")

    candidate = page.locator(".candidates-item.tagged")
    expect(candidate).not_to_have_class(re.compile(r"\bhighlighted\b"))
    expect(candidate).not_to_have_class(re.compile(r"\bmuted\b"))


def test_candidates_are_ordered_by_readiness_and_membership(
    page: Page, candidates_page
):
    create_candidate(name="Muted", is_ready=False, is_member=True)
    create_candidate(name="Ready", is_ready=True, is_member=False)
    create_candidate(name="Highlighted", is_ready=True, is_member=True)
    candidates_page()
    page.goto("/candidates/")

    expect(page.locator(".candidates-item.tagged .candidates-title-link")).to_have_text(
        ["Highlighted", "Ready", "Muted"]
    )


def test_location_is_shown(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", regions=["Brno"])
    candidates_page()
    page.goto("/candidates/")

    candidate = page.locator(".candidates-item.tagged")
    expect(candidate.locator(".candidates-info")).to_have_text("Brno")
    expect(candidate.locator("[data-candidates-tag-type='location']")).to_have_text(
        ["#brno"]
    )


@pytest.mark.parametrize(
    "location_fuzzy",
    [
        None,
        {"locations": [], "is_universal": True},
        {
            "locations": [
                {"raw": r, "place": r, "region": r, "country_code": "CZ"}
                for r in ["Brno", "Praha", "Ostrava"]
            ],
            "is_universal": False,
        },
    ],
    ids=["unknown", "universal", "too_many"],
)
def test_candidate_without_specific_location_can_work_anywhere(
    page: Page, candidates_page, location_fuzzy: dict | None
):
    """
    Regression: candidates without a specific location used to have no location
    at all, so they could never match a location filter
    """
    create_candidate(name="Ada Lovelace", location_fuzzy=location_fuzzy)
    candidates_page()
    page.goto("/candidates/")

    candidate = page.locator(".candidates-item.tagged")
    expect(candidate.locator(".candidates-info")).to_have_text("všudezdejší")
    expect(candidate.locator("[data-candidates-tag-type='location']")).to_have_text(
        ["#kdekoliv"]
    )


def test_tags_list_skills_location_and_languages(page: Page, candidates_page):
    create_candidate(
        name="Ada Lovelace",
        regions=["Hradec Králové"],
        skills=["Python", "SQL"],
        languages=["English", "Deutsch"],
    )
    candidates_page()
    page.goto("/candidates/")

    tags = page.locator(".candidates-item.tagged .candidates-tag")
    expect(tags).to_have_text(
        ["#python", "#sql", "#hradeckralove", "#english", "#deutsch"]
    )


@pytest.mark.parametrize(
    "projects_count, label",
    [
        (1, "1 projekt"),
        (3, "3 projekty"),
        (5, "5 projektů"),
    ],
)
def test_projects_badge(page: Page, candidates_page, projects_count: int, label: str):
    candidate = create_candidate(name="Ada Lovelace")
    for _ in range(projects_count):
        create_candidate_project(candidate)
    candidates_page()
    page.goto("/candidates/")

    badges = page.locator(".candidates-item.tagged .candidates-badge")
    expect(badges).to_have_count(1)
    expect(badges).to_have_text(label)


def test_no_badges_without_projects(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace")
    candidates_page()
    page.goto("/candidates/")

    expect(page.locator(".candidates-badge")).to_have_count(0)


@pytest.mark.parametrize(
    "university, label",
    [
        ("it", "IT VŠ"),
        ("math", "matematická VŠ"),
        pytest.param(
            "electro",
            "elektro VŠ",
            marks=pytest.mark.xfail(
                reason=(
                    "Bug: the badge is looked up as 'ele', but eggtray "
                    "and school_text use 'electro'"
                ),
                strict=True,
                raises=AssertionError,
            ),
        ),
    ],
)
def test_university_badge(page: Page, candidates_page, university: str, label: str):
    create_candidate(name="Ada Lovelace", university=university)
    candidates_page()
    page.goto("/candidates/")

    badges = page.locator(".candidates-item.tagged .candidates-badge")
    expect(badges).to_have_text([label])


@pytest.mark.parametrize("university", ["non_it", None])
def test_no_university_badge_for_other_schools(
    page: Page, candidates_page, university: str | None
):
    create_candidate(name="Ada Lovelace", university=university)
    candidates_page()
    page.goto("/candidates/")

    expect(page.locator(".candidates-badge")).to_have_count(0)


@pytest.mark.xfail(
    reason=(
        "Bug: the stretched title link covers the badges of a closed candidate, "
        "so their tooltips can't be shown, even though the cursor suggests help"
    ),
    strict=True,
    raises=TimeoutError,
)
def test_hovering_badge_shows_tooltip(page: Page, candidates_page):
    candidate = create_candidate(name="Ada Lovelace")
    create_candidate_project(candidate)
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-badge").hover(timeout=2_000)

    tooltip = page.locator(".tooltip.candidates-badge-tooltip")
    expect(tooltip).to_be_visible()
    expect(tooltip).to_have_text("Počet připnutých projektů na GitHubu")


@pytest.mark.parametrize(
    "secondary_school, university, text",
    [
        ("it", None, "IT střední"),
        ("non_it", None, "střední"),
        ("electro", None, "elektro střední"),
        ("it", "it", "IT střední, IT vysoká"),
        ("non_it", "it", "IT vysoká"),
        ("electro", "it", "IT vysoká"),
        ("non_it", "math", "matematická vysoká"),
        ("it", "math", "IT střední, matematická vysoká"),
        (None, "it", "IT vysoká"),
        (None, "non_it", "vysoká"),
    ],
)
def test_school(
    page: Page,
    candidates_page,
    secondary_school: str | None,
    university: str | None,
    text: str,
):
    """
    Regression: candidates without secondary school used to break the page
    """
    create_candidate(
        name="Ada Lovelace", secondary_school=secondary_school, university=university
    )
    candidates_page()
    page.goto("/candidates/")

    candidate = page.locator(".candidates-item.tagged")
    candidate.locator(".candidates-title-link").click()
    school = candidate.locator(".candidates-details", has_text="Škola")
    expect(school.locator(".candidate-details-item")).to_have_text(text)


def test_school_is_shown_only_if_known(page: Page, candidates_page):
    """
    Regression: candidates without any school used to have an empty section
    """
    create_candidate(name="Ada Lovelace")
    candidates_page()
    page.goto("/candidates/")

    candidate = page.locator(".candidates-item.tagged")
    candidate.locator(".candidates-title-link").click()
    expect(candidate.locator(".candidates-details-heading")).to_have_count(0)


def test_details(page: Page, candidates_page):
    candidate = create_candidate(
        name="Ada Lovelace",
        experience=["volunteering", "employee"],
        domains=["finance", "zdravotnictví"],
    )
    create_candidate_project(candidate)
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()
    details = item.locator(".candidates-details")
    expect(details.locator(".candidates-details-heading")).to_have_text(
        ["Praxe", "Čemu také rozumí"]
    )
    expect(details.first.locator(".candidate-details-item")).to_have_text(
        "vlastní projekty, dobrovolnictví v IT, práce v IT"
    )
    expect(details.last.locator(".candidate-details-item")).to_have_text(
        ["finance", "zdravotnictví"]
    )


def test_report_is_linked_only_if_candidate_is_not_ready(page: Page, candidates_page):
    report_url = "https://github.com/juniorguru/eggtray/issues/42"
    create_candidate(name="Ada Lovelace", is_ready=False, report_url=report_url)
    create_candidate(name="Grace Hopper", is_ready=True)
    candidates_page()
    page.goto("/candidates/")

    not_ready = page.locator(".candidates-item.tagged", has_text="Ada Lovelace")
    not_ready.locator(".candidates-title-link").click()
    report = not_ready.locator(".candidates-details", has_text="Co chybí doladit")
    expect(report.locator("a")).to_have_attribute("href", report_url)
    expect(report.locator("a")).to_have_text("github.com/juniorguru/eggtray#42")

    ready = page.locator(".candidates-item.tagged", has_text="Grace Hopper")
    ready.locator(".candidates-title-link").click()
    expect(ready.locator(".candidates-details", has_text="Co chybí")).to_have_count(0)


def test_only_two_projects_are_shown(page: Page, candidates_page):
    candidate = create_candidate(name="Ada Lovelace")
    create_candidate_project(candidate, title="First", priority=1)
    create_candidate_project(candidate, title="Third", priority=3)
    create_candidate_project(candidate, title="Second", priority=2)
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()
    expect(item.locator(".candidates-project-heading")).to_have_text(
        ["First", "Second"]
    )


def test_project_title_falls_back_to_repo_name_without_emoji(
    page: Page, candidates_page
):
    candidate = create_candidate(name="Ada Lovelace")
    create_candidate_project(candidate, title="🐍 Snake Game")
    create_candidate_project(
        candidate, name="ada/todo-app", source_url="https://github.com/ada/todo-app/"
    )
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()
    expect(item.locator(".candidates-project-heading")).to_have_text(
        ["Snake Game", "todo-app"]
    )


def test_project_without_description(page: Page, candidates_page):
    """
    Regression: projects without description used to say 'None'
    """
    candidate = create_candidate(name="Ada Lovelace")
    create_candidate_project(candidate, description=None)
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()
    expect(item.locator(".candidates-project-text")).to_have_text(
        "2 měsíce práce, hotovo 2025"
    )


def test_project_with_demo(page: Page, candidates_page):
    candidate = create_candidate(name="Ada Lovelace")
    create_candidate_project(
        candidate,
        name="ada/game",
        demo_url="https://example.com/game",
        description="Hra pro děti",
    )
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()
    expect(item.locator(".candidates-project-text")).to_contain_text("Hra pro děti")
    links = item.locator(".candidates-project-link")
    expect(links).to_have_text(["Ukázka", "Zdrojový kód"])
    expect(links.first).to_have_attribute("href", "https://example.com/game")
    expect(links.first).to_have_class(re.compile(r"\bprimary\b"))
    expect(links.last).to_have_attribute("href", "https://github.com/ada/game")
    expect(links.last).not_to_have_class(re.compile(r"\bprimary\b"))


def test_project_without_demo(page: Page, candidates_page):
    candidate = create_candidate(name="Ada Lovelace")
    create_candidate_project(candidate, name="ada/lib")
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    item.locator(".candidates-title-link").click()
    links = item.locator(".candidates-project-link")
    expect(links).to_have_text(["Zdrojový kód"])
    expect(links).to_have_class(re.compile(r"\bprimary\b"))
