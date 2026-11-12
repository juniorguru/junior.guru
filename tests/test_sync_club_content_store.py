from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from jg.coop.sync.club_content.store import parse_member


def create_member(**kwargs) -> SimpleNamespace:
    return SimpleNamespace(
        **{
            "id": 123,
            "bot": False,
            "avatar": "https://example.com/avatar.png",
            "display_name": "Alice",
            "mention": "<@123>",
            "joined_at": datetime(2023, 8, 29, 10, 20, tzinfo=UTC),
            "roles": [SimpleNamespace(id=42), SimpleNamespace(id=38)],
            **kwargs,
        }
    )


def test_parse_member():
    assert parse_member(create_member()) == {
        "id": 123,
        "is_bot": False,
        "is_member": True,
        "has_avatar": True,
        "display_name": "Alice",
        "mention": "<@123>",
        "joined_at": datetime(2023, 8, 29, 10, 20),
        "initial_roles": [42, 38],
    }


@pytest.mark.parametrize("avatar, expected", [(None, False), ("https://x", True)])
def test_parse_member_has_avatar(avatar, expected):
    assert parse_member(create_member(avatar=avatar))["has_avatar"] is expected


def test_parse_member_is_bot():
    assert parse_member(create_member(bot=True))["is_bot"] is True
