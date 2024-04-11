import pytest

from jg.coop.lib.cli import command_name


@pytest.mark.parametrize(
    "module, expected_name",
    [
        ("stories", "stories"),
        ("jg.coop.sync.stories", "stories"),
        ("jg.coop.sync.club_content", "club-content"),
    ],
)
def test_command_name(module, expected_name):
    assert command_name(module) == expected_name
