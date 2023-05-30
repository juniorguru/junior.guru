from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Job
from juniorguru.jobs.legacy_jobs.pipelines.database import Pipeline


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


@pytest.fixture
def pipeline(db):
    return Pipeline(db=db, model=Job)


def test_database(db, pipeline, item, spider):
    pipeline.process_item(item, spider)
    with db:
        job = Job.select()[0]

    assert len(job.id) == 56  # sha224 hex digest length
    assert job.source == 'dummy'  # spider name


def test_database_id_prefilled(db, pipeline, item, spider):
    item['id'] = 'honza42'
    pipeline.process_item(item, spider)
    with db:
        job = Job.select()[0]

    assert job.id == 'honza42'


def test_database_id(db, pipeline, item, spider):
    pipeline.process_item(item, spider)
    with db:
        job = Job.select()[0]

    assert len(job.id) == 56  # sha224 hex digest length
