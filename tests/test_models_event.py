from datetime import datetime, timedelta

import pytest

from jg.coop.models.club import ClubUser
from jg.coop.models.event import Event, EventSpeaking

from testing_utils import prepare_test_db


def create_member(id):
    return ClubUser.create(id=id, display_name=f"Jane Doe {id}", mention=f"<#{id}>")


def create_event(id, **kwargs):
    return Event.create(
        id=id,
        **{
            "title": f"Event #{id}",
            "description": "Markdown **description** of the _event_.",
            "bio_name": "Jane Doe",
            "bio": "Jane Doe is so anonymous that we do not really know anything about her.",
            "start_at": datetime.now(),
            "end_at": datetime.now() + timedelta(hours=1),
            **kwargs,
        },
    )


@pytest.fixture
def test_db():
    yield from prepare_test_db([Event, EventSpeaking, ClubUser])


def test_archive_listing(test_db):
    event1 = create_event(1, start_at=datetime(2021, 4, 15))
    event2 = create_event(2, start_at=datetime(2021, 5, 1))
    create_event(3, start_at=datetime(2021, 5, 3))
    event4 = create_event(4, start_at=datetime(2021, 3, 15))

    assert list(Event.archive_listing(now=datetime(2021, 5, 2))) == [
        event2,
        event1,
        event4,
    ]


def test_archive_listing_time(test_db):
    event1 = create_event(1, start_at=datetime(2021, 5, 2, 11))
    create_event(2, start_at=datetime(2021, 5, 2, 22))

    assert list(Event.archive_listing(now=datetime(2021, 5, 2, 18))) == [event1]


def test_planned_listing(test_db):
    create_event(1, start_at=datetime(2021, 4, 15))
    event2 = create_event(2, start_at=datetime(2021, 6, 1))
    event3 = create_event(3, start_at=datetime(2021, 5, 3))
    create_event(4, start_at=datetime(2021, 3, 15))

    assert list(Event.planned_listing(now=datetime(2021, 5, 2))) == [event3, event2]


def test_planned_listing_time(test_db):
    create_event(1, start_at=datetime(2021, 5, 2, 11))
    event2 = create_event(2, start_at=datetime(2021, 5, 2, 22))

    assert list(Event.planned_listing(now=datetime(2021, 5, 2, 18))) == [event2]


def test_list_speaking_members(test_db):
    event1 = create_event(1)
    member1 = create_member(1)
    EventSpeaking.create(event=event1, speaker=member1)

    event2 = create_event(2)
    member2 = create_member(2)
    member3 = create_member(3)
    EventSpeaking.create(event=event2, speaker=member2)
    EventSpeaking.create(event=event2, speaker=member3)

    create_member(4)

    assert set(Event.list_speaking_members()) == {member1, member2, member3}


def test_url(test_db):
    event = create_event(1)

    assert event.url == "https://junior.guru/events/1/"
