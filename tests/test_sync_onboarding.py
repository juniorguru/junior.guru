from datetime import datetime, timedelta, date

import pytest

from juniorguru.lib.club import JUNIORGURU_BOT
from juniorguru.models.club import ClubMessage, ClubUser
from juniorguru.sync.onboarding import prepare_messages


SCHEDULED_MESSAGES = {
    '👋': 'First message',
    '🌯': 'Second message',
    '💤': 'Third message',
    '🆗': 'Fourth message',
    '🟡': 'Fifth message',
    '🟥': 'Sixth message',
    '🤡': 'Seventh message',
}


def create_message(id, author_id, content, created_at=None):
    author = ClubUser(id=author_id, display_name=f'Author #{author_id}', mention='...', tag='...')
    return ClubMessage(id=id,
                       url='https://example.com',
                       content=content,
                       created_at=created_at or datetime(2022, 1, 1),
                       author=author,
                       channel_id=123,
                       channel_name='dan-srb-tipy',
                       channel_mention='...')


def create_bot_message(id, content, created_at=None):
    return create_message(id, JUNIORGURU_BOT, content, created_at)


@pytest.fixture
def today():
    return date.today()


def test_prepare_messages_empty_history(today):
    history = []

    assert prepare_messages(history, SCHEDULED_MESSAGES, today) == [(None, '👋 First message')]


def test_prepare_messages_history_with_no_bot_messages(today):
    history = [create_message(1, 123, 'Non-relevant message'),
               create_message(2, 345, 'Another non-relevant message')]

    assert prepare_messages(history, SCHEDULED_MESSAGES, today) == [(None, '👋 First message')]


def test_prepare_messages_history_with_non_relevant_bot_messages(today):
    history = [create_bot_message(1, 'Non-relevant message'),
               create_bot_message(2, 'Another non-relevant message')]

    assert prepare_messages(history, SCHEDULED_MESSAGES, today) == [(None, '👋 First message')]


def test_prepare_messages_history_with_the_first_message(today):
    history = [create_bot_message(1, '👋 First message')]

    assert prepare_messages(history, SCHEDULED_MESSAGES, today) == [(None, '🌯 Second message')]


def test_prepare_messages_history_with_missing_messages(today):
    history = [create_bot_message(1, '👋 First message'),
               create_bot_message(2, '🟥 Sixth message')]

    assert prepare_messages(history, SCHEDULED_MESSAGES, today) == [(None, '🌯 Second message')]


def test_prepare_messages_history_with_edits(today):
    history = [create_bot_message(1, '👋 Outdated message'),
               create_bot_message(2, '🌯 Second message'),
               create_bot_message(3, '💤 Third message'),
               create_bot_message(4, '🆗 Outdated message')]

    assert prepare_messages(history, SCHEDULED_MESSAGES, today) == [(1, '👋 First message'),
                                                                    (4, '🆗 Fourth message'),
                                                                    (None, '🟡 Fifth message')]


def test_prepare_messages_post_for_the_first_time_that_day(today):
    history = [create_bot_message(1, '👋 First message', created_at=datetime.utcnow() - timedelta(days=3)),
               create_bot_message(2, '🌯 Second message', created_at=datetime.utcnow() - timedelta(days=2)),
               create_bot_message(3, '💤 Third message', created_at=datetime.utcnow() - timedelta(days=1))]

    assert prepare_messages(history, SCHEDULED_MESSAGES, today) == [(None, '🆗 Fourth message')]



def test_prepare_messages_dont_post_twice_the_same_day(today):
    history = [create_bot_message(1, '👋 First message', created_at=datetime.utcnow() - timedelta(days=2)),
               create_bot_message(2, '🌯 Second message', created_at=datetime.utcnow() - timedelta(days=1)),
               create_bot_message(3, '💤 Third message', created_at=datetime.utcnow())]

    assert prepare_messages(history, SCHEDULED_MESSAGES, today) == []


def test_prepare_messages_edit_messages_regardless_of_dates(today):
    history = [create_bot_message(1, '👋 Outdated message', created_at=datetime.utcnow() - timedelta(days=3)),
               create_bot_message(2, '🌯 Second message', created_at=datetime.utcnow() - timedelta(days=2)),
               create_bot_message(3, '💤 Third message', created_at=datetime.utcnow() - timedelta(days=1)),
               create_bot_message(4, '🆗 Outdated message', created_at=datetime.utcnow())]

    assert prepare_messages(history, SCHEDULED_MESSAGES, today) == [(1, '👋 First message'),
                                                                    (4, '🆗 Fourth message')]
