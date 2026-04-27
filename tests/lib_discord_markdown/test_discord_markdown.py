from pathlib import Path

import pytest

from jg.coop.lib.discord_markdown import to_discord_markdown


fixtures = [
    pytest.param(path, id=path.stem) for path in Path(__file__).parent.glob("*.html")
]
assert len(fixtures) > 0, "No fixtures found"


@pytest.mark.parametrize("html_path", fixtures)
def test_to_discord_markdown(html_path: Path):
    html = html_path.read_text()
    expected = html_path.with_suffix(".md").read_text()

    assert to_discord_markdown(html) == expected
