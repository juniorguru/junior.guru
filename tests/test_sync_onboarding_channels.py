from collections import namedtuple

from juniorguru.models.club import ClubUser
from juniorguru.sync.onboarding.channels import prepare_channels_operations


StubTextChannel = namedtuple('StubTextChannel', ['name', 'topic'])


def create_member(id):
    return ClubUser(id=id, display_name='Alice Foo', mention='...', tag='...')


def test_prepare_channels_operations_declutter():
    channel1 = StubTextChannel('honza-tipy', 'Tipy a soukromý kanál jen pro tebe! #abcd')
    channel2 = StubTextChannel('foo-moo-boo', '')

    assert prepare_channels_operations([channel1, channel2], []) == [
        ('delete', (channel1,)),
        ('delete', (channel2,)),
    ]


def test_prepare_channels_operations_empty_category():
    member1 = create_member(1)
    member2 = create_member(2)
    member3 = create_member(3)

    assert prepare_channels_operations([], [member1, member2, member3]) == [
        ('create', (member1,)),
        ('create', (member2,)),
        ('create', (member3,)),
    ]


def test_prepare_channels_operations_close_channels_for_missing_members():
    channel1 = StubTextChannel('alice-foo-tipy', 'Tipy a soukromý kanál jen pro tebe! 🦸 Alice Foo #1')
    channel2 = StubTextChannel('alice-foo-tipy', 'Tipy a soukromý kanál jen pro tebe! 🦸 Alice Foo #2')
    channel3 = StubTextChannel('alice-foo-tipy', 'Tipy a soukromý kanál jen pro tebe! 🦸 Alice Foo #3')
    channels = [channel1, channel2, channel3]

    member1 = create_member(1)
    member3 = create_member(3)
    members = [member1, member3]

    assert prepare_channels_operations(channels, members) == [
        ('update', (member1, channel1)),
        ('update', (member3, channel3)),
        ('close', (channel2,)),
    ]
