from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest
from peewee import SqliteDatabase

from juniorguru.models.podcast import PodcastEpisode


@pytest.fixture
def db_connection():
    models = [PodcastEpisode]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


def test_publish_at_prg():
    podcast_episode = PodcastEpisode(publish_on=date(2023, 2, 10))
    expected = datetime(2023, 2, 10, 1, 42, 42, tzinfo=ZoneInfo('Europe/Prague')).utctimetuple()

    assert podcast_episode.publish_at_prg.utctimetuple() == expected
