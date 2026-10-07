from operator import attrgetter
from types import SimpleNamespace

from jg.coop.sync.roles import (
    calc_stats,
    evaluate_changes,
    repr_ids,
    repr_roles,
    repr_stats,
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
