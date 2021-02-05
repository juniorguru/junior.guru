import pytest
from peewee import SqliteDatabase

from juniorguru.models import Member


@pytest.fixture
def db_connection():
    models = [Member]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


def test_juniorguru_listing(db_connection):
    job1 = Member.create(id='1', avatar_url='https://example.com/avatars/1.png')
    job2 = Member.create(id='2')  # noqa
    job3 = Member.create(id='3', avatar_url='https://example.com/avatars/2.png')
    job4 = Member.create(id='4', avatar_url='https://example.com/avatars/3.png')

    assert list(Member.avatars_listing()) == [job1, job3, job4]
