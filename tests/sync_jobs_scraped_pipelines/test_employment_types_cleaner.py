import pytest

from jg.coop.sync.jobs_scraped.pipelines.employment_types_cleaner import (
    clean_employment_type,
    clean_employment_types,
    is_internship_title,
    process,
)


@pytest.mark.parametrize(
    "employment_type, expected",
    [
        ("brigáda", "temporary"),
        ("částečný úvazek", "parttime"),
        ("Contract", "contract"),
        ("dobrovolnictví", "volunteering"),
        ("dohoda", "temporary"),
        ("external collaboration", "contract"),
        ("full time", "fulltime"),
        ("full-time work", "fulltime"),
        ("Full-time", "fulltime"),
        ("fulltime", "fulltime"),
        ("internship", "internship"),
        ("Internship", "internship"),
        ("jiný typ práce", None),
        ("na dohodu", "temporary"),
        ("na dohodu (brigády)", "temporary"),
        ("neplacená stáž", "internship"),
        ("other", None),
        ("paid internship", "internship"),
        ("part time", "parttime"),
        ("part-time work", "parttime"),
        ("parttime", "parttime"),
        ("placená stáž", "internship"),
        ("plný úvazek", "fulltime"),
        ("práca na plný úväzok", "fulltime"),
        ("práca na skrátený úväzok", "parttime"),
        ("práca na zkrátený úväzok", "parttime"),
        ("práce na plný úvazek", "fulltime"),
        ("práce na zkrácený úvazek", "parttime"),
        ("praxe a stáže", "internship"),
        ("skrátený úväzok", "parttime"),
        ("stáž", "internship"),
        ("temporary", "temporary"),
        ("trainee programs", "internship"),
        ("trainee programy", "internship"),
        ("unpaid internship", "internship"),
        ("volunteering", "volunteering"),
        ("volunteer", "volunteering"),
        ("živnost", "contract"),
        ("živnosť", "contract"),
    ],
)
def test_clean_employment_type(employment_type, expected):
    assert clean_employment_type(employment_type) == expected


def test_clean_employment_type_raises():
    with pytest.raises(ValueError):
        assert clean_employment_type("gargamel")


@pytest.mark.parametrize(
    "item, expected",
    [
        (
            {"employment_types": ["Full-Time"]},
            {"employment_types": ["fulltime"]},
        ),
        (
            {"employment_types": ["part time", "Full-Time"]},
            {"employment_types": ["fulltime", "parttime"]},
        ),
        (
            {"employment_types": ["other", "Full-Time"]},
            {"employment_types": ["fulltime"]},
        ),
        (
            {"employment_types": ["other"]},
            {"employment_types": []},
        ),
        (
            {},
            {},
        ),
        (
            {"title": "Stáž v IT", "employment_types": ["part time"]},
            {"title": "Stáž v IT", "employment_types": ["internship", "parttime"]},
        ),
        (
            {"title": "Software Engineer Intern", "employment_types": ["internship"]},
            {"title": "Software Engineer Intern", "employment_types": ["internship"]},
        ),
        (
            {"title": "Trainee Developer"},
            {"title": "Trainee Developer", "employment_types": ["internship"]},
        ),
        (
            {"title": "Internal Auditor", "employment_types": ["Full-Time"]},
            {"title": "Internal Auditor", "employment_types": ["fulltime"]},
        ),
    ],
)
@pytest.mark.asyncio
async def test_employment_types_cleaner(item, expected):
    item = await process(item)

    assert item == expected


@pytest.mark.parametrize(
    "employment_types, expected",
    [
        (["Full-Time", "dobrovolnictví"], ["fulltime", "volunteering"]),
        (["Full-Time", "full time"], ["fulltime"]),
        (["Full-Time", "part time"], ["fulltime", "parttime"]),
    ],
)
def test_clean_employment_types(employment_types, expected):
    assert clean_employment_types(employment_types) == expected


def test_clean_employment_types_raises():
    with pytest.raises(ValueError):
        assert clean_employment_types(["Full-Time", "Gargamel"])


@pytest.mark.parametrize(
    "title, expected",
    [
        ("Stáž v oblasti IT", True),
        ("IT stážista/stážistka", True),
        ("Placená stáže pro studenty", True),
        ("Software Engineer Intern", True),
        ("Internship – Data Analyst", True),
        ("Interns for QA team", True),
        ("Trainee Software Developer", True),
        ("Graduate Traineeship in IT", True),
        ("Praktikant/ka pro vývoj webu", True),
        ("Praktikantka do IT oddělení", True),
        ("Internal Systems Specialist", False),
        ("International Sales Engineer", False),
        ("Internet Marketing Specialist", False),
        ("Junior Python Developer", False),
        ("", False),
        (None, False),
    ],
)
def test_is_internship_title(title, expected):
    assert is_internship_title(title) is expected
