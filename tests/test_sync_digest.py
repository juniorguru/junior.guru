import pytest
from juniorguru.lib.discord_club import CLUB_GUILD

from juniorguru.sync.digest import format_message, format_channel_digest, format_content, format_channel, calc_reading_time
from juniorguru.models.club import ClubMessage, ClubUser


def test_format_message():
    user = ClubUser(display_name='Honza')
    message = ClubMessage(upvotes_count=3,
                          author=user,
                          channel_name='general',
                          channel_id=123,
                          parent_channel_name='general',
                          parent_channel_id=123,
                          content='Hello world!',
                          url='https://discord.com/channels/123/456/789')

    assert format_message(message) == (
        '3× láska pro **Honza** v #general\n'
        '> Hello world!\n'
        '[Číst příspěvek](https://discord.com/channels/123/456/789)')


def test_format_channel_digest():
    channel_digest = dict(channel_id=123,
                          channel_name='general',
                          parent_channel_id=123,
                          parent_channel_name='general',
                          size=4)

    assert format_channel_digest(channel_digest) == ('**#general**\n'
                                                     '1 minut čtení'
                                                     ' – '
                                                     f'[Číst diskuzi](https://discord.com/channels/{CLUB_GUILD}/123/)')


@pytest.mark.parametrize('content, expected', [
    ('Hello world!', '> Hello world!'),
    ('\n   Hello \n\nworld!\t', '> Hello world!'),
    ('**Hello** _world_!', '> Hello world!'),
    ('Hello world https://honzajavorek.cz!', '> Hello world honzajavorek.cz!'),
    ('Hello world 👨‍👩‍👦 🔥 👻 👾!', '> Hello world 👨‍👩‍👦 🔥 👻 👾!'),
    (('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu nisl diam. '
      'Phasellus sollicitudin vitae nisl sit amet placerat. Nam convallis tincidunt porta!'),
     ('> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu nisl diam. '
      'Phasellus sollicitudin vitae nisl sit amet placerat. Nam convallis…')),
])
def test_format_content(content, expected):
    assert format_content(content) == expected


@pytest.mark.parametrize('channel_id, channel_name, parent_channel_id, parent_channel_name, expected', [
    (1, 'hello-world', 1, 'hello-world', '#hello-world'),
    (1, 'Hello World!', 2, 'general', '#general, vlákno „Hello World!”'),
])
def test_format_channel(channel_id, channel_name, parent_channel_id, parent_channel_name, expected):
    message = ClubMessage(channel_id=channel_id,
                          channel_name=channel_name,
                          parent_channel_id=parent_channel_id,
                          parent_channel_name=parent_channel_name)

    assert format_channel(message) == expected


@pytest.mark.parametrize('content_size, expected', [
    (None, 1),
    (0, 1),
    (20, 1),
    (5000, 4),
])
def test_calc_reading_time(content_size, expected):
    assert calc_reading_time(content_size) == expected
