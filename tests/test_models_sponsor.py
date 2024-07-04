from datetime import date
from typing import Generator

import pytest

from jg.coop.models.base import SqliteDatabase
from jg.coop.models.club import ClubMessage, ClubUser
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
            ClubMessage,
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


@pytest.mark.skip()  # TODO SPONSORS
def test_list_members(test_db: SqliteDatabase, tier_low: SponsorTier):
    member1 = ClubUser.create(display_name="Bob", mention="<@111>", coupon="XEROX")
    member2 = ClubUser.create(display_name="Alice", mention="<@222>", coupon="XEROX")
    ClubUser.create(display_name="Celine", mention="<@333>", coupon="ZALANDO")
    sponsor = create_sponsor("xerox", coupon="XEROX", tier=tier_low)

    assert list(sponsor.list_members) == [member2, member1]


def test_days_until_renew(test_db: SqliteDatabase, tier_low: SponsorTier):
    today = date(2022, 12, 24)
    sponsor = create_sponsor("banana", renews_on=date(2023, 1, 15), tier=tier_low)

    assert sponsor.days_until_renew(today=today) == 22


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


@pytest.mark.skip()  # TODO SPONSORS
def test_tier_grouping():
    pass


@pytest.mark.skip()  # TODO SPONSORS
def test_club_listing():
    pass
