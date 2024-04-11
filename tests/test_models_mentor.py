import pytest

from project.models.club import ClubUser
from project.models.mentor import Mentor

from testing_utils import prepare_test_db


@pytest.fixture
def test_db():
    yield from prepare_test_db([Mentor, ClubUser])


def test_listing(test_db):
    user1 = ClubUser.create(id=123, display_name="Honza", mention="<@111>")
    mentor1 = Mentor.create(id=123, name="Honza J.", topics="a, b, c", user=user1)
    user2 = ClubUser.create(id=456, display_name="Anna", mention="<@222>")
    mentor2 = Mentor.create(id=456, name="Anna K.", topics="x, y, z", user=user2)

    assert list(Mentor.listing()) == [mentor2, mentor1]


@pytest.mark.parametrize(
    "topics, expected",
    [
        ("komunity, HR, příprava na pohovor", True),
        ("Java, JavaScript, TypeScript, Docker, příprava na pohovor", True),
        ("koučování na profesní růst, pohovor nanečisto", True),
        ("datová analýza, Python, Power BI, Excel", False),
    ],
)
def test_interviews_listing(test_db, topics, expected):
    user = ClubUser.create(id=123, display_name="Honza", mention="...")
    mentor = Mentor.create(id=123, name="Honza J.", topics=topics, user=user)

    assert list(Mentor.interviews_listing()) == ([mentor] if expected else [])
