import pytest

from jg.coop.sync.course_providers import (
    TITLE_LENGTH_SEO_LIMIT,
    compile_page_description,
    compile_page_lead,
    compile_page_title,
)


def test_compile_page_title():
    assert compile_page_title("robot_dreams") == (
        "robot_dreams: recenze a zkušenosti absolventů"
    )


def test_compile_page_title_long_name():
    name = "Webařce pod rukou (Magdaléna Boušková)"

    assert compile_page_title(name) == f"{name}: recenze"


@pytest.mark.parametrize(
    "name",
    [
        "Software Development Academy",
        "Webařce pod rukou (Magdaléna Boušková)",
        "Hackni svou budoucnost (David Šetek)",
    ],
)
def test_compile_page_title_fits_limit(name: str):
    assert len(compile_page_title(name)) <= TITLE_LENGTH_SEO_LIMIT


def test_compile_page_title_too_long():
    with pytest.raises(ValueError):
        compile_page_title("x" * TITLE_LENGTH_SEO_LIMIT)


def test_compile_page_description():
    assert compile_page_description("Engeto") == (
        "Recenze a zkušenosti absolventů Engeto. "
        "Vyplatí se? Je to vhodné jako rekvalifikace?"
    )


def test_compile_page_description_extra_questions():
    assert compile_page_description("Czechitas", ["Co Digitální akademie?"]) == (
        "Recenze a zkušenosti absolventů Czechitas. "
        "Vyplatí se? Je to vhodné jako rekvalifikace? Co Digitální akademie?"
    )


def test_compile_page_lead_mentions_recenze():
    assert "recenze" in compile_page_lead("Engeto")
