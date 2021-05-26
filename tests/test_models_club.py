from datetime import datetime, date, timedelta

import pytest
from peewee import SqliteDatabase

from juniorguru.models import ClubMessage, ClubUser
from juniorguru.models.club import INTRO_CHANNEL, JUNIORGURU_BOT


def create_user(id_, **kwargs):
    return ClubUser.create(id=id_,
                           is_member=kwargs.get('is_member', True),
                           is_bot=kwargs.get('is_bot', False),
                           avatar_path=kwargs.get('avatar_path'),
                           display_name=kwargs.get('display_name', 'Kuře Žluté'),
                           mention=kwargs.get('mention', f'<@{id_}>'),
                           joined_at=kwargs.get('joined_at', datetime.now() - timedelta(days=3)))


def create_message(id_, author, **kwargs):
    return ClubMessage.create(id=id_,
                              url=f'https://example.com/messages/{id_}',
                              author=author,
                              content=kwargs.get('content', 'hello'),
                              upvotes_count=kwargs.get('upvotes_count', 0),
                              pins_count=kwargs.get('pins_count', 0),
                              created_at=kwargs.get('created_at', datetime.now() - timedelta(days=3)),
                              channel_id=kwargs.get('channel_id', 123),
                              channel_name=kwargs.get('channel_name', 'random-discussions'),
                              channel_mention=kwargs.get('channel_mention', '<#random-discussions>'),
                              type=kwargs.get('type', 'default'))


@pytest.fixture
def db_connection():
    models = [ClubUser, ClubMessage]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


@pytest.fixture
def juniorguru_bot():
    return create_user(JUNIORGURU_BOT)


def test_message_listing_sort_from_the_oldest(db_connection):
    author = create_user(1)

    message1 = create_message(1, author, created_at=datetime(2021, 10, 1))
    message2 = create_message(2, author, created_at=datetime(2021, 10, 20))
    message3 = create_message(3, author, created_at=datetime(2021, 10, 5))

    assert list(ClubMessage.listing()) == [message1, message3, message2]


def test_message_pins_listing(db_connection):
    author = create_user(1)

    message1 = create_message(1, author, created_at=datetime(2021, 4, 30), pins_count=0)  # noqa
    message2 = create_message(2, author, created_at=datetime(2021, 5, 4), pins_count=5)
    message3 = create_message(3, author, created_at=datetime(2021, 5, 3), pins_count=10)

    assert list(ClubMessage.pins_listing()) == [message3, message2]


def test_message_digest_listing(db_connection):
    author = create_user(1)

    message1 = create_message(1, author, created_at=datetime(2021, 4, 30), upvotes_count=30)  # noqa
    message2 = create_message(2, author, created_at=datetime(2021, 5, 3), upvotes_count=5)
    message3 = create_message(3, author, created_at=datetime(2021, 5, 4), upvotes_count=10)
    message4 = create_message(4, author, created_at=datetime(2021, 5, 5), upvotes_count=4)
    message5 = create_message(5, author, created_at=datetime(2021, 5, 5), upvotes_count=3)  # noqa

    assert list(ClubMessage.digest_listing(date(2021, 5, 1), limit=3)) == [message3, message2, message4]


def test_message_digest_listing_ignores_certain_channels(db_connection):
    author = create_user(1)

    message1 = create_message(1, author, upvotes_count=5)
    message2 = create_message(2, author, upvotes_count=10)
    message3 = create_message(3, author, upvotes_count=20, channel_id=INTRO_CHANNEL)  # noqa

    assert set(ClubMessage.digest_listing(date(2021, 5, 1), limit=3)) == {message1, message2}


def test_message_channel_listing(db_connection):
    author = create_user(1)

    message1 = create_message(1, author, channel_id=333, created_at=datetime(2021, 10, 10))
    message2 = create_message(2, author, channel_id=333, created_at=datetime(2021, 10, 1))
    create_message(3, author, channel_id=222, created_at=datetime(2021, 10, 5))
    create_message(4, author, channel_id=222, created_at=datetime(2021, 10, 20))

    assert list(ClubMessage.channel_listing(333)) == [message2, message1]


def test_author_members_listing(db_connection):
    author1 = create_user(1, is_member=True, is_bot=True)  # noqa
    author2 = create_user(2, is_member=True, is_bot=False)
    author3 = create_user(3, is_member=False, is_bot=True)  # noqa
    author4 = create_user(4, is_member=False, is_bot=False)  # noqa

    assert list(ClubUser.members_listing()) == [author2]


def test_author_top_members_limit_is_five_percent(db_connection):
    for id_ in range(100):
        create_user(id_)

    ClubUser.top_members_limit() == 5


def test_author_top_members_limit_doesnt_count_past_members(db_connection):
    for id_ in range(200):
        create_user(id_, is_member=id_ < 100)

    ClubUser.top_members_limit() == 5


def test_author_top_members_limit_doesnt_count_bots(db_connection):
    for id_ in range(200):
        create_user(id_, is_bot=id_ < 100)

    ClubUser.top_members_limit() == 5


def test_author_top_members_limit_rounds_up(db_connection):
    create_user(1)
    create_user(2)
    create_user(3)

    ClubUser.top_members_limit() == 1


def test_avatars_listing(db_connection):
    user1 = create_user(1, avatar_path='avatars/1.png')
    user2 = create_user(2)  # noqa
    user3 = create_user(3, avatar_path='avatars/2.png')
    user4 = create_user(4, avatar_path='avatars/3.png')

    assert list(ClubUser.avatars_listing()) == [user1, user3, user4]


def test_author_list_recent_messages(db_connection):
    author = create_user(1)

    message1 = create_message(1, author, created_at=datetime(2021, 3, 15))  # noqa
    message2 = create_message(2, author, created_at=datetime(2021, 3, 31))  # noqa
    message3 = create_message(3, author, created_at=datetime(2021, 4, 1))
    message4 = create_message(4, author, created_at=datetime(2021, 4, 15))

    assert list(author.list_recent_messages(today=date(2021, 5, 1))) == [message3, message4]


def test_author_first_seen_on_from_messages(db_connection):
    author = create_user(1, joined_at=datetime(2021, 4, 1))

    create_message(1, author, created_at=datetime(2021, 3, 15))
    create_message(2, author, created_at=datetime(2021, 3, 31))
    create_message(3, author, created_at=datetime(2021, 4, 1))
    create_message(4, author, created_at=datetime(2021, 4, 15))

    assert author.first_seen_on() == date(2021, 3, 15)


def test_author_first_seen_on_from_joined_at(db_connection):
    author = create_user(1, joined_at=datetime(2021, 4, 1))

    assert author.first_seen_on() == date(2021, 4, 1)


@pytest.mark.parametrize('today, expected', [
    (date(2021, 4, 1), True),
    (date(2021, 4, 15), True),
    (date(2021, 4, 16), True),
    (date(2021, 4, 17), False),
    (date(2021, 4, 20), False),
])
def test_author_is_new(db_connection, today, expected):
    author = create_user(1, joined_at=datetime(2021, 4, 1))

    assert author.is_new(today=today) is expected


def test_author_has_intro_false(db_connection):
    author = create_user(1)
    create_message(1, author, channel_id=222)
    create_message(2, author, channel_id=333)

    assert author.has_intro() is False


def test_author_has_intro_true(db_connection):
    author = create_user(1)
    create_message(1, author, channel_id=222)
    create_message(2, author, channel_id=INTRO_CHANNEL)

    assert author.has_intro() is True


def test_author_has_intro_skips_system_message(db_connection):
    author = create_user(1)
    create_message(1, author, channel_id=222)
    create_message(2, author, channel_id=INTRO_CHANNEL, type='new_member')
    create_message(3, author, channel_id=INTRO_CHANNEL, type='premium_guild_subscription')

    assert author.has_intro() is False


def test_author_messages_count(db_connection):
    author = create_user(1)

    create_message(1, author)
    create_message(2, author)
    create_message(3, author)

    assert author.messages_count() == 3


def test_author_recent_messages_count(db_connection):
    author = create_user(1)

    create_message(1, author, created_at=datetime(2021, 2, 15))
    create_message(2, author, created_at=datetime(2021, 3, 10))
    create_message(3, author, created_at=datetime(2021, 3, 15))

    assert author.recent_messages_count(today=date(2021, 4, 1)) == 2


def test_author_upvotes_count(db_connection):
    author = create_user(1)

    create_message(1, author, upvotes_count=1)
    create_message(2, author, upvotes_count=4)
    create_message(3, author, upvotes_count=10)

    assert author.upvotes_count() == 15


def test_author_upvotes_count_skips_some_channels(db_connection):
    author = create_user(1)

    create_message(1, author, upvotes_count=1, channel_id=INTRO_CHANNEL)
    create_message(2, author, upvotes_count=4)
    create_message(3, author, upvotes_count=10)

    assert author.upvotes_count() == 14


def test_author_recent_upvotes_count(db_connection):
    author = create_user(1)

    create_message(1, author, upvotes_count=1, created_at=datetime(2021, 2, 15))
    create_message(2, author, upvotes_count=4, created_at=datetime(2021, 3, 10))
    create_message(3, author, upvotes_count=10, created_at=datetime(2021, 3, 15))

    assert author.recent_upvotes_count(today=date(2021, 4, 1)) == 14


def test_author_recent_upvotes_count_skips_some_channels(db_connection):
    author = create_user(1)

    create_message(1, author, upvotes_count=1, created_at=datetime(2021, 2, 15))
    create_message(2, author, upvotes_count=4, created_at=datetime(2021, 3, 10))
    create_message(3, author, upvotes_count=10, created_at=datetime(2021, 3, 15), channel_id=INTRO_CHANNEL)

    assert author.recent_upvotes_count(today=date(2021, 4, 1)) == 4


def test_last_bot_message_filters_by_channel_id(db_connection, juniorguru_bot):
    message1 = create_message(1, juniorguru_bot, content='🔥 abc', channel_id=123)
    message2 = create_message(2, juniorguru_bot, content='🔥 abc', channel_id=456)  # noqa

    assert ClubMessage.last_bot_message(123, '🔥') == message1


def test_last_bot_message_chooses_bot_message(db_connection, juniorguru_bot):
    message1 = create_message(1, create_user(1), content='🔥 abc', channel_id=123)  # noqa
    message2 = create_message(2, juniorguru_bot, content='🔥 def', channel_id=123)
    message3 = create_message(3, create_user(2), content='🔥 ghe', channel_id=123)  # noqa

    assert ClubMessage.last_bot_message(123, '🔥') == message2


def test_last_bot_message_chooses_last_message(db_connection, juniorguru_bot):
    message1 = create_message(1, juniorguru_bot, content='🔥 abc', channel_id=123)  # noqa
    message2 = create_message(2, juniorguru_bot, content='🔥 def', channel_id=123)

    assert ClubMessage.last_bot_message(123, '🔥') == message2


def test_last_bot_message_filters_by_emoji(db_connection, juniorguru_bot):
    message1 = create_message(1, juniorguru_bot, content='🔥 abc', channel_id=123)
    message2 = create_message(2, juniorguru_bot, content='def', channel_id=123)  # noqa

    assert ClubMessage.last_bot_message(123, '🔥') == message1


def test_last_bot_message_filters_by_emoji_and_text(db_connection, juniorguru_bot):
    message1 = create_message(1, juniorguru_bot, content='🔥 abc', channel_id=123)
    message2 = create_message(2, juniorguru_bot, content='def', channel_id=123)  # noqa
    message3 = create_message(3, juniorguru_bot, content='🔥 ghi', channel_id=123)  # noqa

    assert ClubMessage.last_bot_message(123, '🔥', 'ab') == message1
