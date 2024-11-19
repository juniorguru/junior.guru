from collections import namedtuple

import pytest

from jg.coop.sync.jobs_club import ForumTagName, get_forum_tags


StubForumTag = namedtuple("ForumTag", ["name"])


def test_get_forum_tags():
    mapping = {
        "javascript": ForumTagName.javascript,
        "php": ForumTagName.php,
        "python": ForumTagName.python,
    }
    forum_tags = [
        StubForumTag(ForumTagName.javascript),
        StubForumTag(ForumTagName.php),
        StubForumTag(ForumTagName.python),
    ]
    tech_tags = ["javascript", "php", "python"]

    assert set(get_forum_tags(mapping, forum_tags, tech_tags)) == {
        StubForumTag(ForumTagName.javascript),
        StubForumTag(ForumTagName.php),
        StubForumTag(ForumTagName.python),
    }


def test_get_forum_tags_for_unmapped_tech_tags():
    mapping = {
        "javascript": ForumTagName.javascript,
        "php": ForumTagName.php,
        "python": ForumTagName.python,
    }
    forum_tags = [
        StubForumTag(ForumTagName.javascript),
        StubForumTag(ForumTagName.php),
        StubForumTag(ForumTagName.python),
    ]
    tech_tags = ["javascript", "php", "python", "ruby", "csharp"]

    assert set(get_forum_tags(mapping, forum_tags, tech_tags)) == {
        StubForumTag(ForumTagName.javascript),
        StubForumTag(ForumTagName.php),
        StubForumTag(ForumTagName.python),
    }


def test_get_forum_tags_when_some_forum_tags_are_missing_on_discord():
    mapping = {
        "javascript": ForumTagName.javascript,
        "php": ForumTagName.php,
        "python": ForumTagName.python,
    }
    forum_tags = [
        StubForumTag(ForumTagName.javascript),
        StubForumTag(ForumTagName.php),
    ]
    tech_tags = ["javascript", "php", "python"]

    assert set(get_forum_tags(mapping, forum_tags, tech_tags)) == {
        StubForumTag(ForumTagName.javascript),
        StubForumTag(ForumTagName.php),
    }


def test_get_forum_tags_deals_correctly_with_str_conversion():
    mapping = {
        "javascript": ForumTagName.javascript,
        "php": ForumTagName.php,
    }
    forum_tags = [
        StubForumTag("JavaScript"),
        StubForumTag("PHP"),
    ]
    tech_tags = ["javascript", "php", "python"]

    assert set(get_forum_tags(mapping, forum_tags, tech_tags)) == {
        StubForumTag(ForumTagName.javascript),
        StubForumTag(ForumTagName.php),
    }


@pytest.mark.parametrize(
    "tech_tags, expected",
    [
        (
            ["javascript", "php", "python"],
            {
                StubForumTag(ForumTagName.javascript),
                StubForumTag(ForumTagName.php),
                StubForumTag(ForumTagName.python),
            },
        ),
        (
            ["javascript", "php", "python", "ruby", "csharp"],
            {
                StubForumTag(ForumTagName.javascript),
                StubForumTag(ForumTagName.php),
                StubForumTag(ForumTagName.python),
            },
        ),
        (
            ["javascript", "php", "database", "testing"],
            {
                StubForumTag(ForumTagName.javascript),
                StubForumTag(ForumTagName.php),
                StubForumTag(ForumTagName.testing),
            },
        ),
        (
            ["javascript", "php", "testing", "database"],
            {
                StubForumTag(ForumTagName.javascript),
                StubForumTag(ForumTagName.php),
                StubForumTag(ForumTagName.testing),
            },
        ),
        (
            ["javascript", "php", "database", "python", "testing"],
            {
                StubForumTag(ForumTagName.javascript),
                StubForumTag(ForumTagName.php),
                StubForumTag(ForumTagName.python),
            },
        ),
        (
            ["javascript", "php", "python", "ruby", "csharp", "database", "testing"],
            {
                StubForumTag(ForumTagName.javascript),
                StubForumTag(ForumTagName.php),
                StubForumTag(ForumTagName.python),
            },
        ),
    ],
)
def test_get_forum_tags_outputs_max_tags(
    tech_tags: list[str], expected: set[StubForumTag]
):
    mapping = {
        "databases": ForumTagName.database,
        "javascript": ForumTagName.javascript,
        "php": ForumTagName.php,
        "python": ForumTagName.python,
        "ruby": ForumTagName.ruby,
        "swift": ForumTagName.swift,
        "testing": ForumTagName.testing,
    }
    forum_tags = [
        StubForumTag(ForumTagName.database),
        StubForumTag(ForumTagName.javascript),
        StubForumTag(ForumTagName.php),
        StubForumTag(ForumTagName.python),
        StubForumTag(ForumTagName.ruby),
        StubForumTag(ForumTagName.swift),
        StubForumTag(ForumTagName.testing),
    ]
    dispensables = [ForumTagName.database, ForumTagName.testing]

    assert (
        set(
            get_forum_tags(
                mapping,
                forum_tags,
                tech_tags,
                limit=3,
                dispensables=dispensables,
            )
        )
        == expected
    )
