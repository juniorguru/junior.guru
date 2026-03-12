from datetime import UTC, datetime, timedelta, timezone

import pytest

from jg.coop.lib.discord_club import CLUB_EVENTS_CHANNEL_URL
from jg.coop.lib.template_filters import hours
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


def create_event_instance(**kwargs):
    defaults = {
        "id": 1,
        "title": "Event #1",
        "description": "Markdown **description** of the _event_.",
        "bio_name": "Jane Doe",
        "bio": "Jane Doe is so anonymous that we do not really know anything about her.",
        "start_at": datetime(2021, 5, 1, 10),
        "end_at": datetime(2021, 5, 1, 11),
        "plain_poster_path": "events/1-plain.webp",
    }
    return Event(**(defaults | kwargs))


def test_to_video_upcoming_youtube():
    now = datetime(2021, 5, 2, 10)
    event = create_event_instance(
        start_at=datetime(2021, 5, 3, 10),
        public_recording_url="https://youtube.com/watch?v=abc",
    )

    assert event.to_video(now=now) == {
        "url": CLUB_EVENTS_CHANNEL_URL,
        "button_text": "Připoj se 3.5. v 12:00",
        "badge_icon": "youtube",
        "badge_text": "Veřejný stream",
    }


def test_to_video_upcoming_discord():
    now = datetime(2021, 5, 2, 10)
    event = create_event_instance(
        start_at=datetime(2021, 5, 4, 9, 30),
        public_recording_url=None,
    )

    assert event.to_video(now=now) == {
        "url": CLUB_EVENTS_CHANNEL_URL,
        "button_text": "Připoj se 4.5. v 11:30",
        "badge_icon": "discord",
        "badge_text": "Pouze pro členy",
    }


def test_to_video_past_public():
    now = datetime(2021, 5, 2, 10)
    event = create_event_instance(
        start_at=datetime(2021, 5, 1, 10),
        public_recording_url="https://youtube.com/watch?v=abc",
        public_recording_duration_s=3600,
    )

    assert event.to_video(now=now) == {
        "url": event.public_recording_url,
        "button_text": f"Pusť si {hours(3600)} záznam",
        "badge_icon": "unlock-fill",
        "badge_text": "Veřejný záznam",
    }


def test_to_video_past_private():
    now = datetime(2021, 5, 2, 10)
    event = create_event_instance(
        start_at=datetime(2021, 5, 1, 10),
        club_recording_url="https://discord.com/channels/1/2/3",
        private_recording_duration_s=1800,
    )

    assert event.to_video(now=now) == {
        "url": event.club_recording_url,
        "button_text": f"Pusť si {hours(1800)} záznam",
        "badge_icon": "lock-fill",
        "badge_text": "Pouze pro členy",
    }


def test_to_video_past_without_recording():
    now = datetime(2021, 5, 2, 10)
    event = create_event_instance(start_at=datetime(2021, 5, 1, 10))

    assert event.to_video(now=now) == {
        "url": None,
        "button_text": None,
        "badge_icon": "camera-video-off",
        "badge_text": "Záznam není dostupný",
    }


def test_is_past_with_naive_datetime():
    event = create_event_instance(start_at=datetime(2021, 5, 1, 10))

    assert event.is_past(now=datetime(2021, 5, 2, 10)) is True


def test_is_past_with_utc_datetime():
    event = create_event_instance(start_at=datetime(2021, 5, 1, 10))

    assert event.is_past(now=datetime(2021, 5, 2, 10, tzinfo=UTC)) is True


def test_is_past_with_non_utc_datetime_raises_value_error():
    event = create_event_instance(start_at=datetime(2021, 5, 1, 10))

    with pytest.raises(ValueError, match="UTC"):
        event.is_past(now=datetime(2021, 5, 2, 12, tzinfo=timezone(timedelta(hours=2))))


def test_to_video_with_non_utc_datetime_raises_value_error():
    event = create_event_instance(start_at=datetime(2021, 5, 1, 10))

    with pytest.raises(ValueError, match="UTC"):
        event.to_video(
            now=datetime(2021, 5, 2, 12, tzinfo=timezone(timedelta(hours=2)))
        )
