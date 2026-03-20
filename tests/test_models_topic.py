from typing import Generator

import pytest

from jg.coop.models.base import SqliteDatabase
from jg.coop.models.topic import TopicDiscussion, TopicMention

from testing_utils import prepare_test_db


@pytest.fixture
def test_db() -> Generator[SqliteDatabase, None, None]:
    yield from prepare_test_db([TopicMention, TopicDiscussion])


def test_listing_skips_topic_discussions_without_name(test_db: SqliteDatabase):
    topic1 = TopicDiscussion.create(
        name="Python",
        icon="python",
        monthly_letters_count=200,
    )
    TopicDiscussion.create(
        name=None,
        icon=None,
        monthly_letters_count=300,
    )
    topic2 = TopicDiscussion.create(
        name="JavaScript",
        icon="javascript",
        monthly_letters_count=100,
    )

    assert list(TopicDiscussion.listing()) == [topic1, topic2]
