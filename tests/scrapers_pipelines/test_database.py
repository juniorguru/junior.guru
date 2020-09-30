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


def test_database_company_logo_path(item, spider, db):
    item['company_logos'] = [
        {
            'checksum': '6b874bd7b996e9323fd2e094be83ca4c',
            'path': 'company-logos/d40730d4068db31a09687ebb42f7637e26864a30.png',
            'status': 'uptodate',
            'url': 'https://www.startupjobs.cz/uploads/d6e95f8c946b72f36783aa0a0238341b.png'
        },
        {
            'checksum': 'f3e2f82d7d8b24367f0a2c24b3d1aea3',
            'path': 'company-logos/d1eed8447fb59dc9587dd97148a109a3cca77ed8.png',
            'status': 'uptodate',
            'url': 'https://www.startupjobs.cz/uploads/GQ1A8RDZWYUJfavicon155377551420.png'
        },
    ]
    Pipeline(db=db, model=Job).process_item(item, spider)
    with db:
        job = Job.select()[0]

    assert job.company_logo_path == 'images/company-logos/d40730d4068db31a09687ebb42f7637e26864a30.png'


def test_database_id_prefilled(item, spider, db):
    item['id'] = 'honza42'
    Pipeline(db=db, model=Job).process_item(item, spider)
    with db:
        job = Job.select()[0]

    assert job.id == 'honza42'


def test_database_id_prefilled_no_link(item, spider, db):
    item['id'] = 'honza42'
    del item['link']
    Pipeline(db=db, model=Job).process_item(item, spider)
    with db:
        job = Job.select()[0]

    assert job.id == 'honza42'


def test_database_id_no_location(item, spider, db):
    item['location'] = None
    Pipeline(db=db, model=Job).process_item(item, spider)
    with db:
        job = Job.select()[0]

    assert len(job.id) == 56  # sha224 hex digest length


def test_database_same_link_items(item, spider, db):
    for location in ['Ostrava', 'Brno', 'Pardubice']:
        item['location'] = location
        Pipeline(db=db, model=Job).process_item(item, spider)
    with db:
        jobs = Job.select()

    assert len(jobs) == 3
    assert len({job.id for job in jobs}) == 3
    assert len({job.location for job in jobs}) == 3
