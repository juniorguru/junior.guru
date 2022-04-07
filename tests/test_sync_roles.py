from collections import namedtuple
from operator import attrgetter

from juniorguru.sync.roles import (calc_stats, evaluate_changes, repr_ids, repr_roles,
                                   repr_stats)


DummyRole = namedtuple('Role', ['name'])
DummyMember = namedtuple('Member', ['id', 'display_name', 'upvotes_count'], defaults=[0])


def test_repr_roles():
    roles = [DummyRole('admin'),
             DummyRole('member'),
             DummyRole('hero')]

    assert repr_roles(roles) == "['admin', 'member', 'hero']"


def test_repr_ids():
    members = [DummyMember(1, 'Zuzka'),
               DummyMember(2, 'Honza'),
               DummyMember(3, 'Ondřej')]

    assert repr_ids(members, [1, 2]) == "['Zuzka', 'Honza']"


def test_repr_stats():
    members = [DummyMember(1, 'Zuzka'),
               DummyMember(2, 'Honza'),
               DummyMember(3, 'Ondřej')]
    stats = {1: 42, 2: 420}

    assert repr_stats(members, stats) == "{'Zuzka': 42, 'Honza': 420}"


def test_calc_stats():
    members = [DummyMember(1, 'Zuzka', 20),
               DummyMember(2, 'Honza', 1),
               DummyMember(3, 'Ondřej', 5)]

    assert calc_stats(members, attrgetter('upvotes_count'), 1) == {1: 20}


def test_calc_stats_higher_top_limit():
    members = [DummyMember(1, 'Zuzka', 20),
               DummyMember(2, 'Honza', 1),
               DummyMember(3, 'Ondřej', 5)]

    assert calc_stats(members, attrgetter('upvotes_count'), 2) == {1: 20, 3: 5}


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

    assert evaluate_changes(member_id, member_roles, role_members_ids, role_id) == [(1, 'add', 222)]


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

    assert evaluate_changes(member_id, member_roles, role_members_ids, role_id) == [(1, 'remove', 222)]
