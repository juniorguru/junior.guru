from collections.abc import Generator
from datetime import date

import pytest

from jg.coop.models.base import SqliteDatabase
from jg.coop.models.job import JobTag, ListedJob, Tag, TagType, group_tags_by_type

from testing_utils import prepare_test_db


@pytest.fixture
def test_db() -> Generator[SqliteDatabase]:
    yield from prepare_test_db([ListedJob, JobTag])


def create_job(title: str, *tags: tuple[str, str], **kwargs) -> ListedJob:
    job = ListedJob.create(
        title=title,
        posted_on=kwargs.get("posted_on", date(2026, 1, 1)),
        lang="cs",
        description_html="",
        description_text="",
        description_discord="",
        url=f"https://example.com/{title}",
        company_name="Firma",
    )
    for type, slug in tags:
        JobTag.create(job=job, type=type, slug=slug)
    return job


def test_tagged_listing(test_db: SqliteDatabase):
    create_job("JS", ("technology", "javascript"))
    create_job("TS", ("technology", "typescript"))
    create_job("Python", ("technology", "python"))

    jobs = ListedJob.tagged_listing(TagType.TECHNOLOGY, ["javascript", "typescript"])

    assert {job.title for job in jobs} == {"JS", "TS"}


def test_tagged_listing_job_with_several_matching_tags_once(test_db: SqliteDatabase):
    create_job("Full-stack", ("technology", "javascript"), ("technology", "typescript"))

    jobs = ListedJob.tagged_listing(TagType.TECHNOLOGY, ["javascript", "typescript"])

    assert [job.title for job in jobs] == ["Full-stack"]


def test_tagged_listing_matches_type(test_db: SqliteDatabase):
    create_job("Weird", ("source", "python"))

    assert list(ListedJob.tagged_listing(TagType.TECHNOLOGY, ["python"])) == []


def test_tagged_listing_keeps_order(test_db: SqliteDatabase):
    create_job("Old", ("technology", "python"), posted_on=date(2026, 1, 1))
    create_job("New", ("technology", "python"), posted_on=date(2026, 2, 1))

    jobs = ListedJob.tagged_listing(TagType.TECHNOLOGY, ["python"])

    assert [job.title for job in jobs] == ["New", "Old"]


def test_tags_by_type(test_db: SqliteDatabase):
    create_job("A", ("technology", "python"), ("location", "brno"))
    create_job("B", ("technology", "java"), ("technology", "python"))

    assert ListedJob.tags_by_type() == {
        "location": [Tag(slug="brno", type=TagType.LOCATION)],
        "technology": [
            Tag(slug="java", type=TagType.TECHNOLOGY),
            Tag(slug="python", type=TagType.TECHNOLOGY),
        ],
    }


def test_tags_by_type_of_given_jobs(test_db: SqliteDatabase):
    create_job("A", ("technology", "python"), ("location", "brno"))
    create_job("B", ("technology", "java"), ("location", "praha"))
    jobs = ListedJob.tagged_listing(TagType.TECHNOLOGY, ["python"])

    assert ListedJob.tags_by_type(jobs) == {
        "location": [Tag(slug="brno", type=TagType.LOCATION)],
        "technology": [Tag(slug="python", type=TagType.TECHNOLOGY)],
    }


def test_group_tags_by_type():
    tags = [
        Tag(slug="python", type=TagType.TECHNOLOGY),
        Tag(slug="brno", type=TagType.LOCATION),
        Tag(slug="java", type=TagType.TECHNOLOGY),
    ]

    assert group_tags_by_type(tags) == {
        "location": [Tag(slug="brno", type=TagType.LOCATION)],
        "technology": [
            Tag(slug="python", type=TagType.TECHNOLOGY),
            Tag(slug="java", type=TagType.TECHNOLOGY),
        ],
    }
