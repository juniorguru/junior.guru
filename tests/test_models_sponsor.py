from datetime import date
from typing import Generator

import pytest

from jg.coop.models.base import SqliteDatabase
from jg.coop.models.club import ClubMessage, ClubUser
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.sponsor import Sponsor, SponsorTier

from testing_utils import (
    prepare_course_provider_data,
    prepare_sponsor_data,
    prepare_test_db,
)


def create_sponsor(slug: str, **kwargs) -> Sponsor:
    return Sponsor.create(**prepare_sponsor_data(slug, **kwargs))


@pytest.fixture
def test_db() -> Generator[SqliteDatabase, None, None]:
    yield from prepare_test_db(
        [
            Sponsor,
            SponsorTier,
            ClubUser,
            ClubMessage,
            CourseProvider,
        ]
    )


@pytest.fixture
def tier_low() -> SponsorTier:
    return SponsorTier.create(slug="low", name="LOW", description="...", priority=1)


@pytest.fixture
def tier_mid() -> SponsorTier:
    return SponsorTier.create(slug="mid", name="MID", description="...", priority=2)


@pytest.fixture
def tier_top() -> SponsorTier:
    return SponsorTier.create(slug="top", name="TOP", description="...", priority=3)


def test_sponsor_name_markdown_bold(test_db: SqliteDatabase, tier_low: SponsorTier):
    sponsor = create_sponsor("banana", name="Banana Company", tier=tier_low)

    assert sponsor.name_markdown_bold == "**Banana Company**"


def test_sponsor_course_provider(test_db: SqliteDatabase, tier_low: SponsorTier):
    sponsor = create_sponsor("apple", tier=tier_low)
    course_provider = CourseProvider.create(
        **prepare_course_provider_data(456, slug="apple", sponsor=sponsor)
    )

    assert sponsor.course_provider == course_provider


def test_sponsor_course_provider_is_none(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    sponsor = create_sponsor("apple", tier=tier_low)

    assert sponsor.course_provider is None


def test_sponsor_list_members(test_db: SqliteDatabase, tier_low: SponsorTier):
    member1 = ClubUser.create(display_name="Bob", mention="<@111>", coupon="XEROX")
    member2 = ClubUser.create(display_name="Alice", mention="<@222>", coupon="XEROX")
    ClubUser.create(display_name="Celine", mention="<@333>", coupon="ZALANDO")
    sponsor = create_sponsor("xerox", coupon="XEROX", tier=tier_low)

    assert list(sponsor.list_members) == [member2, member1]


def test_sponsor_days_until_renew(test_db: SqliteDatabase, tier_low: SponsorTier):
    today = date(2022, 12, 24)
    sponsor = create_sponsor("banana", renews_on=date(2023, 1, 15), tier=tier_low)

    assert sponsor.days_until_renew(today=today) == 22


def test_sponsor_handbook_listing(
    test_db: SqliteDatabase,
    tier_low: SponsorTier,
    tier_mid: SponsorTier,
    tier_top: SponsorTier,
):
    create_sponsor("banana", tier=tier_low)
    create_sponsor("apple", tier=tier_mid)
    sponsor3 = create_sponsor("orange", tier=tier_top)
    sponsor4 = create_sponsor("lemon", tier=tier_top)

    assert list(Sponsor.handbook_listing()) == [sponsor4, sponsor3]


def test_sponsor_coupons(test_db: SqliteDatabase, tier_low: SponsorTier):
    create_sponsor("banana", coupon="BANANA", tier=tier_low)
    create_sponsor("apple", coupon="APPLE", tier=tier_low)
    create_sponsor("orange", coupon="ORANGE", tier=tier_low)
    create_sponsor("lemon", coupon="LEMON", tier=tier_low)

    assert Sponsor.coupons() == {"BANANA", "APPLE", "ORANGE", "LEMON"}


def test_sponsor_get_for_course_provider_cz_business_id(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    create_sponsor("banana", cz_business_id=789, tier=tier_low)
    sponsor = create_sponsor("apple", cz_business_id=123, tier=tier_low)
    create_sponsor("orange", cz_business_id=456, tier=tier_low)

    assert Sponsor.get_for_course_provider("xyz", cz_business_id=123) == sponsor


def test_sponsor_get_for_course_provider_cz_business_id_no_match(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    create_sponsor("banana", cz_business_id=789, tier=tier_low)
    create_sponsor("apple", cz_business_id=123, tier=tier_low)
    create_sponsor("orange", cz_business_id=456, tier=tier_low)

    with pytest.raises(Sponsor.DoesNotExist):
        Sponsor.get_for_course_provider("xyz", cz_business_id=999)


def test_sponsor_get_for_course_provider_sk_business_id(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    create_sponsor("banana", sk_business_id=789, tier=tier_low)
    sponsor = create_sponsor("apple", sk_business_id=123, tier=tier_low)
    create_sponsor("orange", sk_business_id=456, tier=tier_low)

    assert Sponsor.get_for_course_provider("xyz", sk_business_id=123) == sponsor


def test_sponsor_get_for_course_provider_sk_business_id_no_match(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    create_sponsor("banana", sk_business_id=789, tier=tier_low)
    create_sponsor("apple", sk_business_id=123, tier=tier_low)
    create_sponsor("orange", sk_business_id=456, tier=tier_low)

    with pytest.raises(Sponsor.DoesNotExist):
        Sponsor.get_for_course_provider("xyz", sk_business_id=999)


def test_sponsor_get_for_course_provider_slug(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    create_sponsor("banana", tier=tier_low)
    sponsor = create_sponsor("apple", tier=tier_low)
    create_sponsor("orange", tier=tier_low)

    assert Sponsor.get_for_course_provider("apple") == sponsor


def test_sponsor_get_for_course_provider_slug_no_match(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    create_sponsor("banana", tier=tier_low)
    create_sponsor("apple", tier=tier_low)
    create_sponsor("orange", tier=tier_low)

    with pytest.raises(Sponsor.DoesNotExist):
        Sponsor.get_for_course_provider("xyz")


def test_sponsor_get_for_course_provider_cz_business_id_trumps_sk_business_id(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    sponsor = create_sponsor(
        "cz", cz_business_id=123, sk_business_id=123, tier=tier_low
    )
    create_sponsor("sk", cz_business_id=789, sk_business_id=789, tier=tier_low)

    assert (
        Sponsor.get_for_course_provider("xyz", cz_business_id=123, sk_business_id=789)
        == sponsor
    )


def test_sponsor_get_for_course_provider_cz_business_id_trumps_slug(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    sponsor = create_sponsor("cz", cz_business_id=123, tier=tier_low)
    create_sponsor("sk", cz_business_id=789, tier=tier_low)

    assert Sponsor.get_for_course_provider("sk", cz_business_id=123) == sponsor


def test_sponsor_get_for_course_provider_sk_business_id_trumps_slug(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    create_sponsor("cz", sk_business_id=123, tier=tier_low)
    sponsor = create_sponsor("sk", sk_business_id=789, tier=tier_low)

    assert Sponsor.get_for_course_provider("sk", sk_business_id=789) == sponsor


def test_sponsor_get_for_course_provider_slug_decides_if_cz_business_ids_are_equal(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    sponsor = create_sponsor("apple", cz_business_id=123, tier=tier_low)
    create_sponsor("banana", cz_business_id=123, tier=tier_low)

    assert Sponsor.get_for_course_provider("apple", cz_business_id=123) == sponsor


def test_sponsor_get_for_course_provider_slug_decides_if_sk_business_ids_are_equal(
    test_db: SqliteDatabase, tier_low: SponsorTier
):
    sponsor = create_sponsor("apple", sk_business_id=123, tier=tier_low)
    create_sponsor("banana", sk_business_id=123, tier=tier_low)

    assert Sponsor.get_for_course_provider("apple", sk_business_id=123) == sponsor
