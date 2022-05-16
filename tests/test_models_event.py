from datetime import date, datetime

import pytest
from peewee import SqliteDatabase

from juniorguru.models.club import ClubUser
from juniorguru.models.event import Event, EventSpeaking


def create_member(id):
    return ClubUser.create(id=id,
                           display_name=f"Jane Doe {id}",
                           mention=f"<#{id}>",
                           tag='abc#1234')


def create_event(id, **kwargs):
    return Event.create(id=id, **{
        'title': f"Event #{id}",
        'description': 'Markdown **description** of the _event_.',
        'bio_name': 'Jane Doe',
        'bio': 'Jane Doe is so anonymous that we do not really know anything about her.',
        'start_at': datetime.now(),
    **kwargs})


@pytest.fixture
def db_connection():
    models = [Event, EventSpeaking, ClubUser]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


def test_archive_listing(db_connection):
    event1 = create_event(1, start_at=datetime(2021, 4, 15))
    event2 = create_event(2, start_at=datetime(2021, 5, 1))
    event3 = create_event(3, start_at=datetime(2021, 5, 3))  # noqa
    event4 = create_event(4, start_at=datetime(2021, 3, 15))

    assert list(Event.archive_listing(today=date(2021, 5, 2))) == [event2, event1, event4]


def test_planned_listing(db_connection):
    event1 = create_event(1, start_at=datetime(2021, 4, 15))  # noqa
    event2 = create_event(2, start_at=datetime(2021, 6, 1))
    event3 = create_event(3, start_at=datetime(2021, 5, 3))
    event4 = create_event(4, start_at=datetime(2021, 3, 15))  # noqa

    assert list(Event.planned_listing(today=date(2021, 5, 2))) == [event3, event2]


def test_next(db_connection):
    event1 = create_event(1, start_at=datetime(2021, 4, 15))  # noqa
    event2 = create_event(2, start_at=datetime(2021, 5, 1))  # noqa
    event3 = create_event(3, start_at=datetime(2021, 5, 3))
    event4 = create_event(4, start_at=datetime(2021, 3, 15))  # noqa

    assert Event.next(today=date(2021, 5, 2)) == event3


def test_next_many_planned(db_connection):
    event1 = create_event(1, start_at=datetime(2021, 4, 15))  # noqa
    event2 = create_event(2, start_at=datetime(2021, 6, 1))  # noqa
    event3 = create_event(3, start_at=datetime(2021, 5, 3))
    event4 = create_event(4, start_at=datetime(2021, 3, 15))  # noqa

    assert Event.next(today=date(2021, 5, 2)) == event3


def test_next_nothing_planned(db_connection):
    create_event(1, start_at=datetime(2021, 4, 15))
    create_event(2, start_at=datetime(2021, 5, 1))
    create_event(4, start_at=datetime(2021, 3, 15))

    assert Event.next(today=date(2021, 5, 2)) is None


def test_list_speaking_members(db_connection):
    event1 = create_event(1)
    member1 = create_member(1)
    EventSpeaking.create(event=event1, speaker=member1)

    event2 = create_event(2)
    member2 = create_member(2)
    member3 = create_member(3)
    EventSpeaking.create(event=event2, speaker=member2)
    EventSpeaking.create(event=event2, speaker=member3)

    member4 = create_member(4)  # noqa

    assert set(Event.list_speaking_members()) == {member1, member2, member3}


def test_url(db_connection):
    event = create_event(1, start_at=datetime(2021, 5, 17, 16, 30, 00))

    assert event.url == 'https://junior.guru/events/#2021-05-17T18-30-00'


def test_slug(db_connection):
    event = create_event(1, start_at=datetime(2021, 5, 17, 16, 30, 00))

    assert event.slug == '2021-05-17T18-30-00'
