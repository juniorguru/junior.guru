import pytest

from juniorguru.fetch.members import is_default_avatar


@pytest.mark.parametrize('url,expected', [
    ('https://cdn.discordapp.com/avatars/524854651644936192/b807c46b5da690cc3365c1fc50159872.webp?size=1024', False),
    ('https://cdn.discordapp.com/embed/avatars/4.png', True),
])
def test_is_default_avatar(url, expected):
    assert is_default_avatar(url) == expected
