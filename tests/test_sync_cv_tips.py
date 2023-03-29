from collections import namedtuple

import pytest

from juniorguru.lib.discord_club import ClubMemberID
from juniorguru.sync import cv_tips


StubMessage = namedtuple('Message', ['author', 'content'])

StubMember = namedtuple('Member', ['id', 'roles'],
                        defaults=dict(roles=[]))


@pytest.mark.parametrize('message, expected', [
    (StubMessage(StubMember(123), 'Hello!'), False),
    (StubMessage(StubMember(123), '💡 Hello!'), False),
    (StubMessage(StubMember(ClubMemberID.BOT), 'Hello!'), False),
    (StubMessage(StubMember(ClubMemberID.BOT), '💡 Hello!'), True),
])
def test_is_message_bot_reminder(message, expected):
    assert cv_tips.is_message_bot_reminder(message) is expected
