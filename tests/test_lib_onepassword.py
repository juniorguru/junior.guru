import json

import pytest

from jg.coop.lib.onepassword import (
    OnePasswordItem,
    build_command,
    parse_link,
    parse_password,
)


ITEM = OnePasswordItem(account="ACC123", vault="vault123", item="item456")


@pytest.mark.parametrize(
    "link, expected",
    [
        ("~/.memberful/trusted_browser", None),
        ("/tmp/trusted_browser", None),
        (
            "https://start.1password.com/open/i?a=ACC123&v=vault123&i=item456&h=example.1password.com",
            ITEM,
        ),
    ],
)
def test_parse_link(link: str, expected: OnePasswordItem | None):
    assert parse_link(link) == expected


def test_parse_link_incomplete():
    with pytest.raises(ValueError):
        parse_link("https://start.1password.com/open/i?a=ACC123&v=vault123")


@pytest.mark.parametrize(
    "fields, expected",
    [
        (
            [
                {"id": "username", "purpose": "USERNAME", "value": "kure"},
                {"id": "password", "purpose": "PASSWORD", "value": "abc123"},
            ],
            "abc123",
        ),
        ([{"id": "password", "purpose": "PASSWORD"}], None),
        ([{"id": "password", "purpose": "PASSWORD", "value": ""}], None),
        ([{"id": "notesPlain", "purpose": "NOTES", "value": "x"}], None),
    ],
)
def test_parse_password(fields: list[dict], expected: str | None):
    item_json = json.dumps({"id": "item456", "fields": fields})

    assert parse_password(item_json) == expected


@pytest.mark.parametrize(
    "subcommand, args, expected",
    [
        (
            "get",
            ("--format", "json"),
            [
                "op",
                "item",
                "get",
                "item456",
                "--format",
                "json",
                "--vault",
                "vault123",
                "--account",
                "ACC123",
            ],
        ),
        (
            "edit",
            ("password=abc123",),
            [
                "op",
                "item",
                "edit",
                "item456",
                "password=abc123",
                "--vault",
                "vault123",
                "--account",
                "ACC123",
            ],
        ),
    ],
)
def test_build_command(subcommand: str, args: tuple[str, ...], expected: list[str]):
    assert build_command(ITEM, subcommand, *args) == expected
