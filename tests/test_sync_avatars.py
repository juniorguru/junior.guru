import pytest

from juniorguru.sync.avatars import is_default_avatar


@pytest.mark.parametrize('url, expected', [
    ('https://honzajavorek.cz/', False),
    ('https://cdn.discordapp.com/avatars/789257286962118688/1ad56dfad2e91692f15e23dcd9520fec.png?size=1024', False),
    ('https://cdn.discordapp.com/embed/avatars/3.png', True),
])
def test_is_default_avatar(url, expected):
    assert is_default_avatar(url) is expected
