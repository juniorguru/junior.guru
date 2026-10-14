from collections.abc import Generator

import pytest

from jg.coop.models.base import SqliteDatabase
from jg.coop.models.club import ClubUser
from jg.coop.models.role import DocumentedRole, InterestRole

from testing_utils import prepare_test_db, prepare_user_data


def create_user(id_, **kwargs) -> ClubUser:
    return ClubUser.create(**prepare_user_data(id_, **kwargs))


@pytest.fixture
def test_db() -> Generator[SqliteDatabase]:
    yield from prepare_test_db([ClubUser, InterestRole, DocumentedRole])


def test_interests(test_db):
    role1 = InterestRole.create(
        club_id=1111,
        name="Zajímá mě: Python",
        interest_name="Python",
    )
    role2 = InterestRole.create(
        club_id=2222,
        name="Zajímá mě: Java",
        interest_name="Java",
    )
    role3 = InterestRole.create(
        club_id=3333,
        name="Zajímá mě: frontend",
        interest_name="frontend",
    )
    role4 = InterestRole.create(
        club_id=4444,
        name="Zajímá mě: vývoj her",
        interest_name="vývoj her",
    )

    create_user(1, initial_roles=[1111, 3333])
    create_user(2, initial_roles=[1111])
    create_user(3, initial_roles=[2222, 4444, 1111])
    create_user(4, initial_roles=[3333])
    create_user(5, initial_roles=[4444])

    assert InterestRole.interests() == [
        (role1, 3),
        (role3, 2),
        (role4, 2),
        (role2, 1),
    ]


def test_documented_role_to_guide_data(test_db):
    role = DocumentedRole.create(
        club_id=1111,
        name="Kouč",
        mention="<@&1111>",
        slug="coach",
        description="Pomáhá ostatním.",
        position=1,
        emoji="🏋️",
        color=0xFF0000,
        icon_path="icons/coach.png",
    )

    assert role.to_guide_data() == {
        "name": "Kouč",
        "description": "Pomáhá ostatním.",
        "color": 0xFF0000,
        "emoji": "🏋️",
        "icon_path": "icons/coach.png",
    }
