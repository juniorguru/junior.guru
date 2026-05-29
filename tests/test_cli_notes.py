import pytest

from jg.coop.cli.notes import get_handbook_emoji_mapping, parse_emoji


def test_parse_emoji():
    source = "---\ntitle: Learn\nemoji: 🚀\n---\n\n# Heading\n"

    emoji = parse_emoji(source)

    assert emoji == "🚀"


def test_parse_emoji_missing_emoji():
    source = "---\ntitle: Learn\n---\n"

    with pytest.raises(ValueError, match="emoji"):
        parse_emoji(source)


def test_get_handbook_emoji_mapping_returns_absolute_paths(tmp_path):
    source = "---\ntitle: Learn\nemoji: 🚀\n---\n"
    page_path = tmp_path / "learn.md"
    page_path.write_text(source)

    mapping = get_handbook_emoji_mapping([page_path])

    assert mapping == {"🚀": page_path.absolute()}


def test_get_handbook_emoji_mapping_detects_duplicated_emoji(tmp_path):
    source = "---\ntitle: Learn\nemoji: 🚀\n---\n"
    path_a = tmp_path / "a.md"
    path_b = tmp_path / "b.md"
    path_a.write_text(source)
    path_b.write_text(source)

    with pytest.raises(ValueError, match="duplicated"):
        get_handbook_emoji_mapping([path_a, path_b])
