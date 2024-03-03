from operator import attrgetter

from juniorguru.sync.roles import (
    calc_stats,
    evaluate_changes,
    repr_ids,
    repr_roles,
    repr_stats,
)


class StubRole:
    def __init__(self, name: str):
        self.name = name


class StubMember:
    def __init__(self, id: int, display_name: str, upvotes_count: int = 0):
        self.id = id
        self.display_name = display_name
        self.upvotes_count = upvotes_count


def test_repr_roles():
    roles = [StubRole("admin"), StubRole("member"), StubRole("hero")]

    assert repr_roles(roles) == "['admin', 'member', 'hero']"


def test_repr_ids():
    members = [
        StubMember(1, "Zuzka"),
        StubMember(2, "Honza"),
        StubMember(3, "Ondřej"),
    ]

    assert repr_ids(members, [1, 2]) == "['Honza', 'Zuzka']"


def test_repr_ids_case_doesnt_matter():
    members = [
        StubMember(1, "Zuzka"),
        StubMember(2, "honza"),
        StubMember(3, "ondřej"),
    ]

    assert repr_ids(members, [1, 2]) == "['honza', 'Zuzka']"


def test_repr_stats():
    members = [
        StubMember(1, "Zuzka"),
        StubMember(2, "Honza"),
        StubMember(3, "Ondřej"),
    ]
    stats = {1: 42, 2: 420}

    assert repr_stats(members, stats) == "{'Zuzka': 42, 'Honza': 420}"


def test_calc_stats():
    members = [
        StubMember(1, "Zuzka", 20),
        StubMember(2, "Honza", 1),
        StubMember(3, "Ondřej", 5),
    ]

    assert calc_stats(members, attrgetter("upvotes_count"), 1) == {1: 20}


def test_calc_stats_higher_top_limit():
    members = [
        StubMember(1, "Zuzka", 20),
        StubMember(2, "Honza", 1),
        StubMember(3, "Ondřej", 5),
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
