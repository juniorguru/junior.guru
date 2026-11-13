from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from jg.coop.sync.club_content.store import get_member_data


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


def test_get_member_data():
    assert get_member_data(create_member()) == {
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
def test_get_member_data_has_avatar(avatar, expected):
    assert get_member_data(create_member(avatar=avatar))["has_avatar"] is expected


def test_get_member_data_is_bot():
    assert get_member_data(create_member(bot=True))["is_bot"] is True
