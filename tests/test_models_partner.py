from typing import Generator

import pytest

from jg.coop.models.base import SqliteDatabase
from jg.coop.models.club import ClubUser
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.partner import Partner

from testing_utils import prepare_organization_data, prepare_test_db


def create_partner(slug: str, **kwargs) -> Partner:
    return Partner.create(**prepare_organization_data(slug, **kwargs))


@pytest.fixture
def test_db() -> Generator[SqliteDatabase, None, None]:
    yield from prepare_test_db(
        [
            Partner,
            ClubUser,
            CourseProvider,
        ]
    )


def test_list_members(test_db: SqliteDatabase):
    member1 = ClubUser.create(display_name="Bob", mention="<@111>", account_id=11)
    member2 = ClubUser.create(display_name="Alice", mention="<@222>", account_id=22)
    ClubUser.create(display_name="Celine", mention="<@333>")
    partner = create_partner("xerox", account_ids=[11, 22])

    assert set(partner.list_members) == {member2, member1}


def test_members_count(test_db: SqliteDatabase):
    ClubUser.create(display_name="Bob", mention="<@111>", account_id=11)
    ClubUser.create(display_name="Alice", mention="<@222>", account_id=22)
    ClubUser.create(display_name="Celine", mention="<@333>")
    partner = create_partner("xerox", account_ids=[11, 22])

    assert partner.members_count == 2
