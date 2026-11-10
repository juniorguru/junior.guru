import pytest

from jg.coop.lib.text import emoji_url
from jg.coop.sync.guide_roles import build_role_args


def create_role(emoji: str | None = None) -> dict:
    return {
        "name": "Kouč",
        "description": "Pomáhá ostatním.",
        "color": 0xFF0000,
        "emoji": emoji,
    }


def test_build_role_args_emoji_thumbnail():
    args = build_role_args(create_role("🧠"))

    assert args["embed"].thumbnail.url == emoji_url("🧠")


def test_build_role_args_no_thumbnail():
    args = build_role_args(create_role(None))

    assert args["embed"].thumbnail is None


@pytest.mark.parametrize("emoji", ["🧠", None])
def test_build_role_args_clears_attachments(emoji):
    args = build_role_args(create_role(emoji))

    assert args["file"] is None
