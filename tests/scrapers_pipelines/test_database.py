from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Job
from juniorguru.scrapers.pipelines.database import Pipeline


@pytest.fixture
def db():
    # Using tmp file because we need to test opening and closing a db conn
    # here and the :memory: sqlite db ceases to exist with the conn closed
    tmp_file = NamedTemporaryFile(delete=False)
    db_path = Path(tmp_file.name)
    tmp_file.close()
    db = SqliteDatabase(tmp_file.name)
    with db:
        Job.bind(db)
        Job.create_table()
    yield db
    if db_path.exists():
        db_path.unlink()


def test_database(item, spider, db):
    Pipeline(db=db, model=Job).process_item(item, spider)
    with db:
        job = Job.select()[0]

    assert len(job.id) == 56  # sha224 hex digest length
    assert job.source == 'dummy'  # spider name
    assert job.is_approved is False
