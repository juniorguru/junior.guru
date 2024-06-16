from typing import Generator

import pytest

from jg.coop.models.base import SqliteDatabase
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.sponsor import Sponsor, SponsorTier

from testing_utils import (
    prepare_course_provider_data,
    prepare_sponsor_data,
    prepare_test_db,
)


def create_course_provider(id: int, **kwargs) -> CourseProvider:
    return CourseProvider.create(**prepare_course_provider_data(id, **kwargs))


def create_sponsor(slug: str, **kwargs) -> Sponsor:
    return Sponsor.create(**prepare_sponsor_data(slug, **kwargs))


@pytest.fixture
def test_db() -> Generator[SqliteDatabase, None, None]:
    yield from prepare_test_db([CourseProvider, Sponsor, SponsorTier])


@pytest.fixture
def tier_low() -> SponsorTier:
    return SponsorTier.create(slug="low", name="LOW", description="...", priority=1)


@pytest.fixture
def tier_mid() -> SponsorTier:
    return SponsorTier.create(slug="mid", name="MID", description="...", priority=2)


@pytest.fixture
def tier_top() -> SponsorTier:
    return SponsorTier.create(slug="top", name="TOP", description="...", priority=3)


def test_listing_sorts_alphabetically(
    test_db: SqliteDatabase,
):
    cp1 = create_course_provider(1, name="Cool Courses")
    cp2 = create_course_provider(2, name="Awesome Courses")
    cp3 = create_course_provider(3, name="Wonderful Courses")

    assert list(CourseProvider.listing()) == [cp2, cp1, cp3]


def test_listing_sorts_alphabetically_czech(
    test_db: SqliteDatabase,
):
    cp1 = create_course_provider(1, name="Cool Courses")
    cp2 = create_course_provider(2, name="Awesome Courses")
    cp3 = create_course_provider(3, name="Wonderful Courses")
    cp4 = create_course_provider(4, name="České Kurzy")

    assert list(CourseProvider.listing()) == [cp2, cp1, cp4, cp3]


def test_listing_sorts_alphabetically_case_insensitive(test_db: SqliteDatabase):
    cp1 = create_course_provider(1, name="Cool Courses")
    cp2 = create_course_provider(2, name="awesome Courses")
    cp3 = create_course_provider(3, name="Wonderful Courses")
    cp4 = create_course_provider(4, name="zzz Courses")

    assert list(CourseProvider.listing()) == [cp2, cp1, cp3, cp4]


def test_listing_sorts_sponsors_first(test_db: SqliteDatabase, tier_low: SponsorTier):
    cp1 = create_course_provider(1, name="Cool Courses")
    cp2 = create_course_provider(2, name="Awesome Courses")
    cp3 = create_course_provider(
        3, name="Wonderful Courses", sponsor=create_sponsor("banana", tier=tier_low)
    )

    assert list(CourseProvider.listing()) == [cp3, cp2, cp1]


def test_listing_sorts_sponsors_by_tier_then_by_name(
    test_db: SqliteDatabase,
    tier_low: SponsorTier,
    tier_top: SponsorTier,
):
    sponsor_top = create_sponsor("banana", tier=tier_top)
    sponsor_low = create_sponsor("cherry", tier=tier_low)
    cp1 = create_course_provider(1, name="Cool Courses", sponsor=sponsor_low)
    cp2 = create_course_provider(2, name="Awesome Courses")
    cp3 = create_course_provider(3, name="Wonderful Courses", sponsor=sponsor_top)

    assert list(CourseProvider.listing()) == [cp3, cp1, cp2]
