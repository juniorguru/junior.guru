from collections.abc import Generator
from datetime import date

import pytest

from jg.coop.models.base import SqliteDatabase
from jg.coop.models.club import ClubUser
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.sponsor import Sponsor

from testing_utils import prepare_organization_data, prepare_test_db


def create_sponsor(slug: str, **kwargs) -> Sponsor:
    return Sponsor.create(**prepare_organization_data(slug, **kwargs))


@pytest.fixture
def test_db() -> Generator[SqliteDatabase]:
    yield from prepare_test_db(
        [
            Sponsor,
            ClubUser,
            CourseProvider,
        ]
    )


def test_list_members(test_db: SqliteDatabase):
    member1 = ClubUser.create(display_name="Bob", mention="<@111>", account_id=11)
    member2 = ClubUser.create(display_name="Alice", mention="<@222>", account_id=22)
    ClubUser.create(display_name="Celine", mention="<@333>")
    sponsor = create_sponsor("xerox", account_ids=[11, 22])

    assert set(sponsor.list_members) == {member2, member1}


def test_members_count(test_db: SqliteDatabase):
    ClubUser.create(display_name="Bob", mention="<@111>", account_id=11)
    ClubUser.create(display_name="Alice", mention="<@222>", account_id=22)
    ClubUser.create(display_name="Celine", mention="<@333>")
    sponsor = create_sponsor("xerox", account_ids=[11, 22])

    assert sponsor.members_count == 2


def test_days_until_renew(test_db: SqliteDatabase):
    today = date(2022, 12, 24)
    sponsor = create_sponsor("banana", renews_on=date(2023, 1, 15))

    assert sponsor.days_until_renew(today=today) == 22


def test_listing(
    test_db: SqliteDatabase,
):
    sponsor1 = create_sponsor("banana")
    sponsor2 = create_sponsor("apple")
    sponsor3 = create_sponsor("orange")
    sponsor4 = create_sponsor("lemon")

    assert list(Sponsor.listing()) == [sponsor2, sponsor1, sponsor4, sponsor3]


def test_handbook_listing(
    test_db: SqliteDatabase,
):
    sponsor1 = create_sponsor("banana")
    sponsor2 = create_sponsor("apple")
    sponsor3 = create_sponsor("orange")
    sponsor4 = create_sponsor("lemon")

    assert Sponsor.handbook_listing() == [sponsor2, sponsor1, sponsor4, sponsor3]


def test_handbook_listing_too_many(
    test_db: SqliteDatabase,
):
    create_sponsor("banana")
    create_sponsor("apple")
    create_sponsor("orange")
    create_sponsor("lemon")
    create_sponsor("avocado")

    with pytest.raises(ValueError):
        Sponsor.handbook_listing()


def test_club_listing(
    test_db: SqliteDatabase,
):
    sponsor1 = create_sponsor("banana", account_ids=[11, 22])
    sponsor2 = create_sponsor("apple", account_ids=[11, 22, 33, 44])
    sponsor3 = create_sponsor("orange", account_ids=[11, 22])
    sponsor4 = create_sponsor("lemon", account_ids=[])
    sponsor5 = create_sponsor("avocado", account_ids=[])

    assert list(Sponsor.club_listing()) == [
        sponsor2,
        sponsor1,
        sponsor3,
        sponsor5,
        sponsor4,
    ]


def test_to_guide_data(test_db: SqliteDatabase):
    sponsor = create_sponsor(
        "xerox",
        name="Xerox",
        url="https://xerox.example.com",
        poster_path="posters/xerox.png",
        role_id=123,
        account_ids=[11],
    )

    assert sponsor.to_guide_data() == {
        "name": "Xerox",
        "url": "https://xerox.example.com",
        "role_id": 123,
        "members_count": 1,
        "poster_path": "posters/xerox.png",
    }
