from operator import attrgetter
from types import SimpleNamespace

import pytest

from jg.coop.sync.roles import (
    RoleConfig,
    calc_stats,
    evaluate_changes,
    normalize_emoji,
    repr_ids,
    repr_roles,
    repr_stats,
    resolve_emoji,
)


def test_repr_roles():
    roles = [
        SimpleNamespace(name="admin"),
        SimpleNamespace(name="member"),
        SimpleNamespace(name="hero"),
    ]

    assert repr_roles(roles) == "['admin', 'member', 'hero']"


def test_repr_ids():
    members = [
        SimpleNamespace(id=1, display_name="Zuzka"),
        SimpleNamespace(id=2, display_name="Honza"),
        SimpleNamespace(id=3, display_name="Ondřej"),
    ]

    assert repr_ids(members, [1, 2]) == "['Honza', 'Zuzka']"


def test_repr_ids_case_doesnt_matter():
    members = [
        SimpleNamespace(id=1, display_name="Zuzka"),
        SimpleNamespace(id=2, display_name="honza"),
        SimpleNamespace(id=3, display_name="ondřej"),
    ]

    assert repr_ids(members, [1, 2]) == "['honza', 'Zuzka']"


def test_repr_stats():
    members = [
        SimpleNamespace(id=1, display_name="Zuzka"),
        SimpleNamespace(id=2, display_name="Honza"),
        SimpleNamespace(id=3, display_name="Ondřej"),
    ]
    stats = {1: 42, 2: 420}

    assert repr_stats(members, stats) == "{'Zuzka': 42, 'Honza': 420}"


def test_calc_stats():
    members = [
        SimpleNamespace(id=1, display_name="Zuzka", upvotes_count=20),
        SimpleNamespace(id=2, display_name="Honza", upvotes_count=1),
        SimpleNamespace(id=3, display_name="Ondřej", upvotes_count=5),
    ]

    assert calc_stats(members, attrgetter("upvotes_count"), 1) == {1: 20}


def test_calc_stats_higher_top_limit():
    members = [
        SimpleNamespace(id=1, display_name="Zuzka", upvotes_count=20),
        SimpleNamespace(id=2, display_name="Honza", upvotes_count=1),
        SimpleNamespace(id=3, display_name="Ondřej", upvotes_count=5),
    ]

    assert calc_stats(members, attrgetter("upvotes_count"), 2) == {1: 20, 3: 5}


def test_evaluate_changes_member_should_have_this_role_and_already_has():
    member_id = 1
    member_roles = [222, 333, 444]

    role_id = 222
    role_members_ids = [1, 2, 3, 4]

    assert evaluate_changes(member_id, member_roles, role_members_ids, role_id) == []


def test_evaluate_changes_member_should_have_this_role_but_doesnt():
    member_id = 1
    member_roles = [333, 444]

    role_id = 222
    role_members_ids = [1, 2, 3, 4]

    assert evaluate_changes(member_id, member_roles, role_members_ids, role_id) == [
        (1, "add", 222)
    ]


def test_evaluate_changes_member_shouldnt_have_this_role_and_doesnt():
    member_id = 1
    member_roles = [333, 444]

    role_id = 222
    role_members_ids = [2, 3, 4]

    assert evaluate_changes(member_id, member_roles, role_members_ids, role_id) == []


def test_evaluate_changes_member_shouldnt_have_this_role_but_has():
    member_id = 1
    member_roles = [222, 333, 444]

    role_id = 222
    role_members_ids = [2, 3, 4]

    assert evaluate_changes(member_id, member_roles, role_members_ids, role_id) == [
        (1, "remove", 222)
    ]


def create_role_config(emoji: str | None = None) -> RoleConfig:
    return RoleConfig(id=1, slug="coach", description="Pomáhá ostatním.", emoji=emoji)


@pytest.mark.parametrize(
    "unicode_emoji, config_emoji, expected",
    [
        (None, None, None),
        (None, "🧠", "🧠"),
        ("🧠", "🧠", "🧠"),
        ("🗓", "🗓️", "🗓️"),
        ("🗓️", "🗓", "🗓"),
    ],
)
def test_resolve_emoji(unicode_emoji, config_emoji, expected):
    role = SimpleNamespace(name="Kouč", icon=None, unicode_emoji=unicode_emoji)

    assert resolve_emoji(role, create_role_config(config_emoji)) == expected


@pytest.mark.parametrize(
    "unicode_emoji, config_emoji",
    [
        ("⭐", "🧠"),
        ("⭐", None),
    ],
)
def test_resolve_emoji_raises_on_mismatch(unicode_emoji, config_emoji):
    role = SimpleNamespace(name="Kouč", icon=None, unicode_emoji=unicode_emoji)

    with pytest.raises(ValueError, match="has icon"):
        resolve_emoji(role, create_role_config(config_emoji))


def test_resolve_emoji_raises_on_image_icon():
    role = SimpleNamespace(
        name="Kouč",
        icon=SimpleNamespace(url="https://example.com/icon.png"),
        unicode_emoji=None,
    )

    with pytest.raises(ValueError, match="image icon"):
        resolve_emoji(role, create_role_config("🧠"))


@pytest.mark.parametrize(
    "emoji, expected",
    [
        (None, None),
        ("", None),
        ("🧠", "🧠"),
        ("🗓️", "🗓"),
    ],
)
def test_normalize_emoji(emoji, expected):
    assert normalize_emoji(emoji) == expected
