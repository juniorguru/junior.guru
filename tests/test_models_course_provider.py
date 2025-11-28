from typing import Generator

import pytest

from jg.coop.models.base import SqliteDatabase
from jg.coop.models.course_provider import CourseProvider, CourseProviderGroup
from jg.coop.models.partner import Partner
from jg.coop.models.sponsor import Sponsor, SponsorTier

from testing_utils import (
    prepare_course_provider_data,
    prepare_organization_data,
    prepare_test_db,
)


def create_course_provider(id: int, **kwargs) -> CourseProvider:
    return CourseProvider.create(**prepare_course_provider_data(id, **kwargs))


def create_sponsor(slug: str, **kwargs) -> Sponsor:
    return Sponsor.create(**prepare_organization_data(slug, **kwargs))


def create_partner(slug: str, **kwargs) -> Partner:
    return Partner.create(**prepare_organization_data(slug, **kwargs))


@pytest.fixture
def test_db() -> Generator[SqliteDatabase, None, None]:
    yield from prepare_test_db([CourseProvider, Sponsor, SponsorTier, Partner])


@pytest.fixture
def tier_low() -> SponsorTier:
    return SponsorTier.create(plan_id=11, name="LOW", priority=1)


@pytest.fixture
def tier_mid() -> SponsorTier:
    return SponsorTier.create(plan_id=22, name="MID", priority=2)


@pytest.fixture
def tier_top() -> SponsorTier:
    return SponsorTier.create(plan_id=33, name="TOP", priority=3)


def test_organization_cz_business_id(test_db: SqliteDatabase, tier_low: SponsorTier):
    cp = create_course_provider(1, slug="xyz", cz_business_id=123)
    create_sponsor("banana", cz_business_id=789, tier=tier_low)
    sponsor = create_sponsor("apple", cz_business_id=123, tier=tier_low)
    create_sponsor("orange", cz_business_id=456, tier=tier_low)

    assert cp.organization == sponsor


def test_organization_cz_business_id_no_match(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    cp = create_course_provider(1, slug="xyz", cz_business_id=999)
    create_sponsor("banana", cz_business_id=789, tier=tier_low)
    create_sponsor("apple", cz_business_id=123, tier=tier_low)
    create_sponsor("orange", cz_business_id=456, tier=tier_low)

    assert cp.organization is None


def test_organization_sk_business_id(test_db: SqliteDatabase, tier_low: SponsorTier):
    cp = create_course_provider(1, slug="xyz", sk_business_id=123)
    create_sponsor("banana", sk_business_id=789, tier=tier_low)
    sponsor = create_sponsor("apple", sk_business_id=123, tier=tier_low)
    create_sponsor("orange", sk_business_id=456, tier=tier_low)

    assert cp.organization == sponsor


def test_organization_sk_business_id_no_match(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    cp = create_course_provider(1, slug="xyz", sk_business_id=999)
    create_sponsor("banana", sk_business_id=789, tier=tier_low)
    create_sponsor("apple", sk_business_id=123, tier=tier_low)
    create_sponsor("orange", sk_business_id=456, tier=tier_low)

    assert cp.organization is None


def test_organization_slug(test_db: SqliteDatabase, tier_low: SponsorTier):
    cp = create_course_provider(1, slug="apple")
    create_sponsor("banana", tier=tier_low)
    sponsor = create_sponsor("apple", tier=tier_low)
    create_sponsor("orange", tier=tier_low)

    assert cp.organization == sponsor


def test_organization_slug_no_match(test_db: SqliteDatabase, tier_low: SponsorTier):
    cp = create_course_provider(1, slug="xyz")
    create_sponsor("banana", tier=tier_low)
    create_sponsor("apple", tier=tier_low)
    create_sponsor("orange", tier=tier_low)

    assert cp.organization is None


def test_organization_cz_business_id_trumps_sk_business_id(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    cp = create_course_provider(1, slug="xyz", cz_business_id=123, sk_business_id=789)
    sponsor = create_sponsor(
        "cz", cz_business_id=123, sk_business_id=123, tier=tier_low
    )
    create_sponsor("sk", cz_business_id=789, sk_business_id=789, tier=tier_low)

    assert cp.organization == sponsor


def test_organization_cz_business_id_trumps_slug(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    cp = create_course_provider(1, slug="sk", cz_business_id=123)
    sponsor = create_sponsor("cz", cz_business_id=123, tier=tier_low)
    create_sponsor("sk", cz_business_id=789, tier=tier_low)

    assert cp.organization == sponsor


def test_organization_sk_business_id_trumps_slug(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    cp = create_course_provider(1, slug="sk", sk_business_id=789)
    create_sponsor("cz", sk_business_id=123, tier=tier_low)
    sponsor = create_sponsor("sk", sk_business_id=789, tier=tier_low)

    assert cp.organization == sponsor


def test_organization_slug_decides_if_cz_business_ids_are_equal(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    cp = create_course_provider(1, slug="apple", cz_business_id=123)
    sponsor = create_sponsor("apple", cz_business_id=123, tier=tier_low)
    create_sponsor("banana", cz_business_id=123, tier=tier_low)

    assert cp.organization == sponsor


def test_organization_slug_decides_if_sk_business_ids_are_equal(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    cp = create_course_provider(1, slug="apple", sk_business_id=123)
    sponsor = create_sponsor("apple", sk_business_id=123, tier=tier_low)
    create_sponsor("banana", sk_business_id=123, tier=tier_low)

    assert cp.organization == sponsor


def test_group_others(test_db: SqliteDatabase):
    cp = create_course_provider(1)

    assert cp.group == CourseProviderGroup.OTHERS


def test_group_partner(test_db: SqliteDatabase):
    create_partner("banana", cz_business_id=111)
    cp = create_course_provider(1, cz_business_id=111)

    assert cp.group == CourseProviderGroup.PARTNERS


def test_group_sponsor_others(test_db: SqliteDatabase, tier_mid: SponsorTier):
    create_sponsor("banana", tier=tier_mid, cz_business_id=111)
    cp = create_course_provider(1, cz_business_id=111)

    assert cp.group == CourseProviderGroup.OTHERS


def test_group_sponsor_highlighted(test_db: SqliteDatabase, tier_mid: SponsorTier):
    tier_mid.courses_highlight = True
    tier_mid.save()
    create_sponsor("banana", tier=tier_mid, cz_business_id=111)
    cp = create_course_provider(1, cz_business_id=111)

    assert cp.group == CourseProviderGroup.HIGHLIGHTED


def test_group_graveyard(test_db: SqliteDatabase):
    cp = create_course_provider(1, is_gone=True)

    assert cp.group == CourseProviderGroup.GRAVEYARD


def test_grouping(
    test_db: SqliteDatabase, tier_low: SponsorTier, tier_mid: SponsorTier
):
    create_partner("banana", cz_business_id=111)
    cp1 = create_course_provider(1, cz_business_id=111)

    create_sponsor("pear", tier=tier_low, cz_business_id=222)
    cp2 = create_course_provider(2, name="Pear", cz_business_id=222)

    cp3 = create_course_provider(3, name="Avocado", cz_business_id=333)

    tier_mid.courses_highlight = True
    tier_mid.save()
    create_sponsor("peach", tier=tier_mid, cz_business_id=444)
    cp4 = create_course_provider(4, cz_business_id=444)

    assert CourseProvider.grouping() == [
        (CourseProviderGroup.HIGHLIGHTED, [cp4]),
        (CourseProviderGroup.PARTNERS, [cp1]),
        (CourseProviderGroup.OTHERS, [cp3, cp2]),
    ]


def test_listing_sorts_alphabetically(test_db: SqliteDatabase):
    cp1 = create_course_provider(1, name="Cool Courses")
    cp2 = create_course_provider(2, name="Awesome Courses")
    cp3 = create_course_provider(3, name="Wonderful Courses")

    assert list(CourseProvider.listing()) == [cp2, cp1, cp3]


def test_listing_sorts_alphabetically_czech(test_db: SqliteDatabase):
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
