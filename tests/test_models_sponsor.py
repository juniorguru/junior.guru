from datetime import date
from typing import Generator

import pytest

from jg.coop.models.base import SqliteDatabase
from jg.coop.models.club import ClubUser
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.sponsor import Sponsor, SponsorTier

from testing_utils import prepare_organization_data, prepare_test_db


def create_sponsor(slug: str, **kwargs) -> Sponsor:
    return Sponsor.create(**prepare_organization_data(slug, **kwargs))


@pytest.fixture
def test_db() -> Generator[SqliteDatabase, None, None]:
    yield from prepare_test_db(
        [
            Sponsor,
            SponsorTier,
            ClubUser,
            CourseProvider,
        ]
    )


@pytest.fixture
def tier_low() -> SponsorTier:
    return SponsorTier.create(plan_id=11, name="LOW", priority=1)


@pytest.fixture
def tier_mid() -> SponsorTier:
    return SponsorTier.create(plan_id=22, name="MID", priority=2)


@pytest.fixture
def tier_top() -> SponsorTier:
    return SponsorTier.create(plan_id=33, name="TOP", priority=3)


def test_list_members(test_db: SqliteDatabase, tier_low: SponsorTier):
    member1 = ClubUser.create(display_name="Bob", mention="<@111>", account_id=11)
    member2 = ClubUser.create(display_name="Alice", mention="<@222>", account_id=22)
    ClubUser.create(display_name="Celine", mention="<@333>")
    sponsor = create_sponsor("xerox", tier=tier_low, account_ids=[11, 22])

    assert set(sponsor.list_members) == {member2, member1}


def test_members_count(test_db: SqliteDatabase, tier_low: SponsorTier):
    ClubUser.create(display_name="Bob", mention="<@111>", account_id=11)
    ClubUser.create(display_name="Alice", mention="<@222>", account_id=22)
    ClubUser.create(display_name="Celine", mention="<@333>")
    sponsor = create_sponsor("xerox", tier=tier_low, account_ids=[11, 22])

    assert sponsor.members_count == 2


def test_days_until_renew(test_db: SqliteDatabase, tier_low: SponsorTier):
    today = date(2022, 12, 24)
    sponsor = create_sponsor("banana", renews_on=date(2023, 1, 15), tier=tier_low)

    assert sponsor.days_until_renew(today=today) == 22


def test_listing(
    test_db: SqliteDatabase,
    tier_low: SponsorTier,
    tier_mid: SponsorTier,
    tier_top: SponsorTier,
):
    sponsor1 = create_sponsor("banana", tier=tier_low)
    sponsor2 = create_sponsor("apple", tier=tier_mid)
    sponsor3 = create_sponsor("orange", tier=tier_top)
    sponsor4 = create_sponsor("lemon", tier=tier_top)

    assert list(Sponsor.listing()) == [sponsor4, sponsor3, sponsor2, sponsor1]


def test_handbook_listing(
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


def test_club_listing(
    test_db: SqliteDatabase,
    tier_low: SponsorTier,
    tier_mid: SponsorTier,
    tier_top: SponsorTier,
):
    sponsor1 = create_sponsor("banana", tier=tier_low, account_ids=[11, 22])
    sponsor2 = create_sponsor("apple", tier=tier_mid, account_ids=[11, 22, 33, 44])
    sponsor3 = create_sponsor("orange", tier=tier_top, account_ids=[11, 22])
    sponsor4 = create_sponsor("lemon", tier=tier_top, account_ids=[])
    sponsor5 = create_sponsor("avocado", tier=tier_top, account_ids=[])

    assert list(Sponsor.club_listing()) == [
        sponsor2,
        sponsor3,
        sponsor1,
        sponsor5,
        sponsor4,
    ]


def test_tier_grouping(
    test_db: SqliteDatabase,
    tier_low: SponsorTier,
    tier_mid: SponsorTier,
    tier_top: SponsorTier,
):
    sponsor1 = create_sponsor("banana", tier=tier_low)
    sponsor2 = create_sponsor("apple", tier=tier_mid)
    sponsor3 = create_sponsor("orange", tier=tier_top)
    sponsor4 = create_sponsor("lemon", tier=tier_top)

    assert Sponsor.tier_grouping() == [
        (tier_top, [sponsor4, sponsor3]),
        (tier_mid, [sponsor2]),
        (tier_low, [sponsor1]),
    ]
