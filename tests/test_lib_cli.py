import pytest

from juniorguru.lib.cli import command_name


@pytest.mark.parametrize('module, expected_name', [
    ('stories', 'stories'),
    ('juniorguru.sync.stories', 'stories'),
    ('juniorguru.sync.club_content', 'club-content'),
])
def test_command_name(module, expected_name):
    assert command_name(module) == expected_name
