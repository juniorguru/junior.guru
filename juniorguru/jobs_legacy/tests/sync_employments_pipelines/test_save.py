from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Employment
from juniorguru.jobs.employments.pipelines.save import Pipeline


@pytest.fixture
def db():
    # Using tmp file because we need to test opening and closing a db conn
    # here and the :memory: sqlite db ceases to exist with the conn closed
    tmp_file = NamedTemporaryFile(delete=False)
    db_path = Path(tmp_file.name)
    tmp_file.close()
    db = SqliteDatabase(tmp_file.name)
    with db:
        Employment.bind(db)
        Employment.create_table()
    yield db
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def pipeline(db):
    return Pipeline(db=db, model=Employment)


def test_save_does_not_exist(db, pipeline, item, spider):
    item['title'] = 'XYZ'
    item['url'] = 'https://example.com/jobs/1'
    pipeline.process_item(item, spider)
    with db:
        employments = Employment.select()

    assert len(employments) == 1
    assert employments[0].title == 'XYZ'
    assert employments[0].items_merged_count == 0


def test_save_exists(db, pipeline, item, spider):
    item['title'] = 'XYZ'
    item['url'] = 'https://example.com/jobs/1'
    pipeline.process_item(item, spider)
    pipeline.process_item(item, spider)
    pipeline.process_item(item, spider)
    with db:
        employments = Employment.select()

    assert len(employments) == 1
    assert employments[0].title == 'XYZ'
    assert employments[0].items_merged_count == 2
