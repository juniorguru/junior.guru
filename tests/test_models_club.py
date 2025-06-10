from datetime import date, datetime, timedelta

import pytest

from jg.coop.lib.discord_club import ClubChannelID, ClubMemberID, get_starting_emoji
from jg.coop.models.club import ClubMessage, ClubPin, ClubUser

from testing_utils import prepare_test_db, prepare_user_data


def create_user(id_, **kwargs) -> ClubUser:
    return ClubUser.create(**prepare_user_data(id_, **kwargs))


def create_message(id_, user, **kwargs):
    channel_id = kwargs.get("channel_id", 123)
    created_at = kwargs.get("created_at", datetime.now() - timedelta(days=3))
    content = kwargs.get("content", "hello")
    return ClubMessage.create(
        id=id_,
        url=f"https://example.com/messages/{id_}",
        author=user,
        author_is_bot=user.id == ClubMemberID.BOT,
        content=content,
        content_size=len(content),
        content_starting_emoji=get_starting_emoji(content),
        upvotes_count=kwargs.get("upvotes_count", 0),
        created_at=created_at,
        created_month=kwargs.get("created_month", f"{created_at:%Y-%d}"),
        channel_id=channel_id,
        channel_name=kwargs.get("channel_name", "random-discussions"),
        channel_type=kwargs.get("channel_type", "text"),
        parent_channel_id=kwargs.get("parent_channel_id", channel_id),
        parent_channel_name=kwargs.get("parent_channel_name", "random-discussions"),
        parent_channel_type=kwargs.get("parent_channel_type", "text"),
        type=kwargs.get("type", "default"),
        is_private=kwargs.get("is_private", False),
    )


@pytest.fixture
def test_db():
    yield from prepare_test_db([ClubUser, ClubMessage, ClubPin])


@pytest.fixture
def juniorguru_bot():
    return create_user(ClubMemberID.BOT)


def test_message_listing_sort_from_the_oldest(test_db):
    user = create_user(1)
    message1 = create_message(1, user, created_at=datetime(2021, 10, 1))
    message2 = create_message(2, user, created_at=datetime(2021, 10, 20))
    message3 = create_message(3, user, created_at=datetime(2021, 10, 5))
    create_message(4, user, created_at=datetime(2021, 10, 5), is_private=True)

    assert list(ClubMessage.listing()) == [message1, message3, message2]


def test_message_digest_listing(test_db):
    user = create_user(1)
    create_message(1, user, created_at=datetime(2021, 4, 30), upvotes_count=30)
    message2 = create_message(2, user, created_at=datetime(2021, 5, 3), upvotes_count=5)
    message3 = create_message(
        3, user, created_at=datetime(2021, 5, 4), upvotes_count=10
    )
    message4 = create_message(4, user, created_at=datetime(2021, 5, 5), upvotes_count=4)
    create_message(5, user, created_at=datetime(2021, 5, 5), upvotes_count=3)
    create_message(
        6, user, created_at=datetime(2021, 5, 5), upvotes_count=30, is_private=True
    )

    assert list(ClubMessage.digest_listing(date(2021, 5, 1), limit=3)) == [
        message3,
        message2,
        message4,
    ]


def test_message_digest_listing_ignores_certain_channels(test_db):
    user = create_user(1)
    message1 = create_message(1, user, upvotes_count=5)
    message2 = create_message(2, user, upvotes_count=10)
    create_message(3, user, upvotes_count=20, channel_id=ClubChannelID.INTRO)

    assert set(ClubMessage.digest_listing(date(2021, 5, 1), limit=3)) == {
        message1,
        message2,
    }


def test_message_digest_channels(test_db):
    user = create_user(1)
    for i in range(3):
        create_message(
            10 + i,
            user,
            created_at=datetime(2023, 5, 2),
            content="abcd",
            channel_id=1,
            channel_name="channel-1",
            parent_channel_id=100,
            parent_channel_name="parent-channel-100",
        )
    for i in range(10):
        create_message(
            20 + i,
            user,
            created_at=datetime(2023, 5, 3),
            content="abcd",
            channel_id=2,
            channel_name="channel-2",
            parent_channel_id=200,
            parent_channel_name="parent-channel-200",
        )
    for i in range(5):
        create_message(
            30 + i,
            user,
            created_at=datetime(2023, 5, 4),
            content="abcd",
            channel_id=3,
            channel_name="channel-3",
            parent_channel_id=300,
            parent_channel_name="parent-channel-300",
        )
    digest_channels = list(ClubMessage.digest_channels(date(2023, 5, 1), limit=3))

    assert digest_channels == [
        {
            "size": 10 * 4,
            "channel_id": 2,
            "channel_name": "channel-2",
            "parent_channel_id": 200,
            "parent_channel_name": "parent-channel-200",
        },
        {
            "size": 5 * 4,
            "channel_id": 3,
            "channel_name": "channel-3",
            "parent_channel_id": 300,
            "parent_channel_name": "parent-channel-300",
        },
        {
            "size": 3 * 4,
            "channel_id": 1,
            "channel_name": "channel-1",
            "parent_channel_id": 100,
            "parent_channel_name": "parent-channel-100",
        },
    ]


def test_message_digest_channels_ignores_private_messages(test_db):
    user = create_user(1)
    kwargs = dict(
        created_at=datetime(2023, 5, 2),
        content="abcd",
        channel_id=1,
        channel_name="channel",
        parent_channel_id=100,
        parent_channel_name="parent-channel",
    )
    for i in range(3):
        create_message(10 + i, user, is_private=False, **kwargs)
    for i in range(10):
        create_message(20 + i, user, is_private=True, **kwargs)
    digest_channels = list(ClubMessage.digest_channels(date(2023, 5, 1), limit=3))

    assert digest_channels == [
        {
            "size": 3 * 4,
            "channel_id": 1,
            "channel_name": "channel",
            "parent_channel_id": 100,
            "parent_channel_name": "parent-channel",
        }
    ]


def test_message_digest_channels_ignores_certain_channels(test_db):
    user = create_user(1)
    for i in range(3):
        create_message(
            10 + i,
            user,
            content="abcd",
            created_at=datetime(2023, 5, 2),
            channel_id=123,
            channel_name="Hello Alice!",
            parent_channel_id=ClubChannelID.INTRO,
            parent_channel_name="intro",
        )
    for i in range(10):
        create_message(
            20 + i,
            user,
            content="abcd",
            created_at=datetime(2023, 5, 2),
            channel_id=456,
            channel_name="Blah blah",
            parent_channel_id=100,
            parent_channel_name="parent-channel",
        )
    digest_channels = list(ClubMessage.digest_channels(date(2023, 5, 1), limit=3))

    assert digest_channels == [
        {
            "size": 10 * 4,
            "channel_id": 456,
            "channel_name": "Blah blah",
            "parent_channel_id": 100,
            "parent_channel_name": "parent-channel",
        }
    ]


def test_message_digest_channels_ignores_old_messages(test_db):
    user = create_user(1)
    kwargs = dict(
        content="abcd",
        channel_id=1,
        channel_name="channel",
        parent_channel_id=100,
        parent_channel_name="parent-channel",
    )
    for i in range(3):
        create_message(10 + i, user, created_at=datetime(2023, 4, 29), **kwargs)
    for i in range(10):
        create_message(20 + i, user, created_at=datetime(2023, 5, 2), **kwargs)
    digest_channels = list(ClubMessage.digest_channels(date(2023, 5, 1), limit=3))

    assert digest_channels == [
        {
            "size": 10 * 4,
            "channel_id": 1,
            "channel_name": "channel",
            "parent_channel_id": 100,
            "parent_channel_name": "parent-channel",
        }
    ]


def test_message_channel_listing(test_db):
    user = create_user(1)

    message1 = create_message(
        1, user, channel_id=333, created_at=datetime(2021, 10, 10)
    )
    message2 = create_message(2, user, channel_id=333, created_at=datetime(2021, 10, 1))
    create_message(3, user, channel_id=222, created_at=datetime(2021, 10, 5))
    create_message(4, user, channel_id=222, created_at=datetime(2021, 10, 20))

    assert list(ClubMessage.channel_listing(333)) == [message2, message1]


def test_user_members_listing(test_db):
    create_user(1, is_member=True, is_bot=True)
    user2 = create_user(2, is_member=True, is_bot=False)
    create_user(3, is_member=False, is_bot=True)
    create_user(4, is_member=False, is_bot=False)

    assert list(ClubUser.members_listing()) == [user2]


def test_user_get_member_by_id(test_db):
    user = create_user(2, is_member=True, is_bot=False)

    assert ClubUser.get_member_by_id(2) == user


@pytest.mark.parametrize(
    "is_member, is_bot",
    [
        (True, True),
        (False, True),
        (False, False),
    ],
)
def test_user_get_member_by_id_raises(test_db, is_member, is_bot):
    with pytest.raises(ClubUser.DoesNotExist):
        assert ClubUser.get_member_by_id(2)


def test_user_top_members_limit_is_five_percent(test_db):
    for id_ in range(100):
        create_user(id_)

    ClubUser.top_members_limit() == 5


def test_user_top_members_limit_doesnt_count_past_members(test_db):
    for id_ in range(200):
        create_user(id_, is_member=id_ < 100)

    ClubUser.top_members_limit() == 5


def test_user_top_members_limit_doesnt_count_bots(test_db):
    for id_ in range(200):
        create_user(id_, is_bot=id_ < 100)

    ClubUser.top_members_limit() == 5


def test_user_top_members_limit_rounds_up(test_db):
    create_user(1)
    create_user(2)
    create_user(3)

    ClubUser.top_members_limit() == 1


def test_avatars_listing(test_db):
    user1 = create_user(1, avatar_path="avatars/1.png")
    create_user(2)
    user3 = create_user(3, avatar_path="avatars/2.png")
    user4 = create_user(4, avatar_path="avatars/3.png")

    assert list(ClubUser.avatars_listing()) == [user1, user3, user4]


def test_user_list_recent_messages(test_db):
    user = create_user(1)

    create_message(1, user, created_at=datetime(2021, 3, 15))
    create_message(2, user, created_at=datetime(2021, 3, 31))
    message3 = create_message(3, user, created_at=datetime(2021, 4, 1))
    message4 = create_message(4, user, created_at=datetime(2021, 4, 15))
    create_message(5, user, created_at=datetime(2021, 4, 16), is_private=True)

    assert list(user.list_recent_messages(today=date(2021, 5, 1))) == [
        message4,
        message3,
    ]


def test_user_list_recent_messages_private(test_db):
    user = create_user(1)

    create_message(1, user, created_at=datetime(2021, 3, 15))
    create_message(2, user, created_at=datetime(2021, 3, 31))
    message3 = create_message(3, user, created_at=datetime(2021, 4, 1))
    message4 = create_message(4, user, created_at=datetime(2021, 4, 15))
    message5 = create_message(
        5, user, created_at=datetime(2021, 4, 16), is_private=True
    )

    assert list(user.list_recent_messages(today=date(2021, 5, 1), private=True)) == [
        message5,
        message4,
        message3,
    ]


def test_user_list_public_messages(test_db):
    user = create_user(1)

    create_message(1, user, created_at=datetime(2021, 3, 15), is_private=True)
    create_message(2, user, created_at=datetime(2021, 3, 31), is_private=True)
    message3 = create_message(3, user, created_at=datetime(2021, 4, 1))
    message4 = create_message(4, user, created_at=datetime(2021, 4, 15))

    assert list(user.list_public_messages) == [message4, message3]


def test_user_first_seen_on_from_messages(test_db):
    user = create_user(1, joined_at=datetime(2021, 4, 1))

    create_message(1, user, created_at=datetime(2021, 3, 15))
    create_message(2, user, created_at=datetime(2021, 3, 31))
    create_message(3, user, created_at=datetime(2021, 4, 1))
    create_message(4, user, created_at=datetime(2021, 4, 15))

    assert user.first_seen_on() == date(2021, 3, 15)


def test_user_first_seen_on_respects_messages(test_db):
    user = create_user(1, joined_at=datetime(2021, 4, 1))

    create_message(1, user, created_at=datetime(2021, 4, 15))
    create_message(2, user, created_at=datetime(2021, 8, 30))

    assert user.first_seen_on() == date(2021, 4, 15)


def test_user_first_seen_on_from_joined_at(test_db):
    user = create_user(1, joined_at=datetime(2021, 4, 1))

    assert user.first_seen_on() == date(2021, 4, 1)


def test_user_first_seen_on_from_pins(test_db):
    user1 = create_user(1)
    user2 = create_user(2, joined_at=None)

    message = create_message(1, user1, created_at=datetime(2021, 12, 19))
    ClubPin.create(member=user2, pinned_message=message)

    assert user2.first_seen_on() == date(2021, 12, 19)


@pytest.mark.parametrize(
    "today, expected",
    [
        (date(2021, 4, 1), True),
        (date(2021, 4, 20), True),
        (date(2021, 4, 21), True),
        (date(2021, 4, 22), False),
        (date(2021, 4, 29), False),
    ],
)
def test_user_is_new(test_db, today, expected):
    user = create_user(1, joined_at=datetime(2021, 4, 1))

    assert user.is_new(today=today) is expected


def test_user_intro_doesnt_exist(test_db):
    user = create_user(1)
    create_message(1, user, channel_id=222)
    create_message(2, user, channel_id=333)

    assert user.intro is None


def test_user_intro_exists(test_db):
    user = create_user(1)
    create_message(1, user, channel_id=222)
    create_message(2, user, channel_id=ClubChannelID.INTRO)

    assert user.intro.id == 2


def test_user_intro_skips_system_messages(test_db):
    user = create_user(1)
    create_message(1, user, channel_id=222)
    create_message(2, user, channel_id=ClubChannelID.INTRO, type="new_member")
    create_message(
        3, user, channel_id=ClubChannelID.INTRO, type="premium_guild_subscription"
    )

    assert user.intro is None


def test_user_intro_uses_the_latest_message(test_db):
    created_at = datetime.now() - timedelta(days=1)
    user = create_user(1)
    create_message(
        1,
        user,
        channel_id=ClubChannelID.INTRO,
        created_at=created_at + timedelta(seconds=30),
    )
    create_message(2, user, channel_id=ClubChannelID.INTRO, created_at=created_at)

    assert user.intro.id == 1


def test_user_messages_count(test_db):
    user = create_user(1)

    create_message(1, user)
    create_message(2, user)
    create_message(3, user)
    create_message(4, user, is_private=True)

    assert user.messages_count() == 3


def test_user_messages_count_private(test_db):
    user = create_user(1)

    create_message(1, user)
    create_message(2, user)
    create_message(3, user)
    create_message(4, user, is_private=True)

    assert user.messages_count(private=True) == 4


def test_user_recent_content_size(test_db):
    user = create_user(1)

    create_message(1, user, created_at=datetime(2021, 2, 15), content="0123456789")
    create_message(2, user, created_at=datetime(2021, 3, 10), content="0123456789")
    create_message(3, user, created_at=datetime(2021, 3, 15), content="0123456789")
    create_message(
        4, user, created_at=datetime(2021, 3, 15), content="0123456789", is_private=True
    )

    assert user.recent_content_size(today=date(2021, 4, 1)) == 20


def test_user_recent_content_size_private(test_db):
    user = create_user(1)

    create_message(1, user, created_at=datetime(2021, 2, 15), content="0123456789")
    create_message(2, user, created_at=datetime(2021, 3, 10), content="0123456789")
    create_message(3, user, created_at=datetime(2021, 3, 15), content="0123456789")
    create_message(
        4, user, created_at=datetime(2021, 3, 15), content="0123456789", is_private=True
    )

    assert user.recent_content_size(today=date(2021, 4, 1), private=True) == 30


def test_user_upvotes_count(test_db):
    user = create_user(1)

    create_message(1, user, upvotes_count=1)
    create_message(2, user, upvotes_count=4)
    create_message(3, user, upvotes_count=10)
    create_message(4, user, upvotes_count=300, is_private=True)

    assert user.upvotes_count() == 15


def test_user_upvotes_count_private(test_db):
    user = create_user(1)

    create_message(1, user, upvotes_count=1)
    create_message(2, user, upvotes_count=4)
    create_message(3, user, upvotes_count=10)
    create_message(4, user, upvotes_count=300, is_private=True)

    assert user.upvotes_count(private=True) == 315


def test_user_upvotes_count_skips_some_channels(test_db):
    user = create_user(1)

    create_message(1, user, upvotes_count=1, channel_id=ClubChannelID.INTRO)
    create_message(2, user, upvotes_count=4)
    create_message(3, user, upvotes_count=10)

    assert user.upvotes_count() == 14


def test_user_recent_upvotes_count(test_db):
    user = create_user(1)

    create_message(1, user, upvotes_count=1, created_at=datetime(2021, 2, 15))
    create_message(2, user, upvotes_count=4, created_at=datetime(2021, 3, 10))
    create_message(3, user, upvotes_count=10, created_at=datetime(2021, 3, 15))
    create_message(
        4, user, upvotes_count=300, created_at=datetime(2021, 3, 15), is_private=True
    )

    assert user.recent_upvotes_count(today=date(2021, 4, 1)) == 14


def test_user_recent_upvotes_count_private(test_db):
    user = create_user(1)

    create_message(1, user, upvotes_count=1, created_at=datetime(2021, 2, 15))
    create_message(2, user, upvotes_count=4, created_at=datetime(2021, 3, 10))
    create_message(3, user, upvotes_count=10, created_at=datetime(2021, 3, 15))
    create_message(
        4, user, upvotes_count=300, created_at=datetime(2021, 3, 15), is_private=True
    )

    assert user.recent_upvotes_count(today=date(2021, 4, 1), private=True) == 314


def test_user_recent_upvotes_count_skips_some_channels(test_db):
    user = create_user(1)

    create_message(1, user, upvotes_count=1, created_at=datetime(2021, 2, 15))
    create_message(2, user, upvotes_count=4, created_at=datetime(2021, 3, 10))
    create_message(
        3,
        user,
        upvotes_count=10,
        created_at=datetime(2021, 3, 15),
        channel_id=ClubChannelID.INTRO,
    )

    assert user.recent_upvotes_count(today=date(2021, 4, 1)) == 4


def test_last_bot_message_filters_by_channel_id(test_db, juniorguru_bot):
    message1 = create_message(1, juniorguru_bot, content="🔥 abc", channel_id=123)
    create_message(2, juniorguru_bot, content="🔥 abc", channel_id=456)

    assert ClubMessage.last_bot_message(123, "🔥") == message1


def test_last_bot_message_chooses_bot_message(test_db, juniorguru_bot):
    create_message(1, create_user(1), content="🔥 abc", channel_id=123)
    message2 = create_message(2, juniorguru_bot, content="🔥 def", channel_id=123)
    create_message(3, create_user(2), content="🔥 ghe", channel_id=123)

    assert ClubMessage.last_bot_message(123, "🔥") == message2


def test_last_bot_message_chooses_last_message(test_db, juniorguru_bot):
    create_message(1, juniorguru_bot, content="🔥 abc", channel_id=123)
    message2 = create_message(2, juniorguru_bot, content="🔥 def", channel_id=123)

    assert ClubMessage.last_bot_message(123, "🔥") == message2


def test_last_bot_message_filters_by_emoji(test_db, juniorguru_bot):
    message1 = create_message(1, juniorguru_bot, content="🔥 abc", channel_id=123)
    create_message(2, juniorguru_bot, content="def", channel_id=123)

    assert ClubMessage.last_bot_message(123, "🔥") == message1


def test_last_bot_message_filters_by_emoji_and_text(test_db, juniorguru_bot):
    message1 = create_message(1, juniorguru_bot, content="🔥 abc", channel_id=123)
    create_message(2, juniorguru_bot, content="def", channel_id=123)
    create_message(3, juniorguru_bot, content="🔥 ghi", channel_id=123)

    assert ClubMessage.last_bot_message(123, "🔥", "ab") == message1
