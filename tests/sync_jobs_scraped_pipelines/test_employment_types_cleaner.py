import pytest

from jg.coop.sync.jobs_scraped.pipelines.employment_types_cleaner import (
    clean_employment_type,
    clean_employment_types,
    process,
)


@pytest.mark.parametrize(
    "employment_type, expected",
    [
        ("částečný úvazek", "parttime"),
        ("Contract", "contract"),
        ("dobrovolnictví", "volunteering"),
        ("external collaboration", "contract"),
        ("full time", "fulltime"),
        ("full-time work", "fulltime"),
        ("Full-time", "fulltime"),
        ("fulltime", "fulltime"),
        ("internship", "internship"),
        ("Internship", "internship"),
        ("jiný typ práce", None),
        ("neplacená stáž", "internship"),
        ("other", None),
        ("paid internship", "internship"),
        ("part time", "parttime"),
        ("part-time work", "parttime"),
        ("parttime", "parttime"),
        ("placená stáž", "internship"),
        ("plný úvazek", "fulltime"),
        ("práca na plný úväzok", "fulltime"),
        ("práca na zkrátený úväzok", "parttime"),
        ("práce na plný úvazek", "fulltime"),
        ("práce na zkrácený úvazek", "parttime"),
        ("praxe a stáže", "internship"),
        ("stáž", "internship"),
        ("temporary", "temporary"),
        ("trainee programs", "internship"),
        ("trainee programy", "internship"),
        ("unpaid internship", "internship"),
        ("volunteering", "volunteering"),
        ("volunteer", "volunteering"),
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
            dict(employment_types=["Full-Time"]),
            dict(employment_types=["fulltime"]),
        ),
        (
            dict(employment_types=["part time", "Full-Time"]),
            dict(employment_types=["fulltime", "parttime"]),
        ),
        (
            dict(employment_types=["other", "Full-Time"]),
            dict(employment_types=["fulltime"]),
        ),
        (
            dict(employment_types=["other"]),
            dict(employment_types=[]),
        ),
        (
            dict(),
            dict(),
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
