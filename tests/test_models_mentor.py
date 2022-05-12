import pytest
from peewee import SqliteDatabase

from juniorguru.models.club import ClubUser
from juniorguru.models.mentor import Mentor


@pytest.fixture
def db_connection():
    models = [Mentor, ClubUser]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


def test_listing(db_connection):
    user1 = ClubUser.create(id=123, display_name='Honza', mention='...', tag='...')
    mentor1 = Mentor.create(id=123, name='Honza J.', topics='a, b, c', user=user1)
    user2 = ClubUser.create(id=456, display_name='Anna', mention='...', tag='...')
    mentor2 = Mentor.create(id=456, name='Anna K.', topics='x, y, z', user=user2)

    assert list(Mentor.listing()) == [mentor2, mentor1]


@pytest.mark.parametrize('topics, expected', [
    ('komunity, HR, příprava na pohovor', True),
    ('Java, JavaScript, TypeScript, Docker, příprava na pohovor', True),
    ('koučování na profesní růst, pohovor nanečisto', True),
    ('datová analýza, Python, Power BI, Excel', False),
])
def test_interviews_listing(db_connection, topics, expected):
    user = ClubUser.create(id=123, display_name='Honza', mention='...', tag='...')
    mentor = Mentor.create(id=123, name='Honza J.', topics=topics, user=user)

    assert list(Mentor.interviews_listing()) == ([mentor] if expected else [])
