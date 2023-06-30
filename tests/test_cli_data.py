import gzip
from textwrap import dedent

import pytest

from juniorguru.cli.data import (count_lines, get_row_updates, is_jobs_archive, is_scrapy_cache, make_schema_idempotent,
                                 merge_unique_lines)


def test_make_schema_idempotent():
    assert make_schema_idempotent(dedent('''
        CREATE TABLE "clubdocumentedrole" ("id" INTEGER NOT NULL PRIMARY KEY, "name" VARCHAR(255) NOT NULL, "mention" VARCHAR(255) NOT NULL, "slug" VARCHAR(255) NOT NULL, "description" TEXT NOT NULL, "position" INTEGER NOT NULL, "emoji" VARCHAR(255));
        CREATE TABLE "clubpinreaction" ("id" INTEGER NOT NULL PRIMARY KEY, "user_id" INTEGER NOT NULL, "message_id" INTEGER NOT NULL, FOREIGN KEY ("user_id") REFERENCES "clubuser" ("id"), FOREIGN KEY ("message_id") REFERENCES "clubmessage" ("id"));
        CREATE INDEX "scrapedjob_last_seen_on" ON "scrapedjob" ("last_seen_on");
        CREATE UNIQUE INDEX "scrapedjob_url" ON "scrapedjob" ("url");
    ''')).strip() == dedent('''
        CREATE TABLE IF NOT EXISTS "clubdocumentedrole" ("id" INTEGER NOT NULL PRIMARY KEY, "name" VARCHAR(255) NOT NULL, "mention" VARCHAR(255) NOT NULL, "slug" VARCHAR(255) NOT NULL, "description" TEXT NOT NULL, "position" INTEGER NOT NULL, "emoji" VARCHAR(255));
        CREATE TABLE IF NOT EXISTS "clubpinreaction" ("id" INTEGER NOT NULL PRIMARY KEY, "user_id" INTEGER NOT NULL, "message_id" INTEGER NOT NULL, FOREIGN KEY ("user_id") REFERENCES "clubuser" ("id"), FOREIGN KEY ("message_id") REFERENCES "clubmessage" ("id"));
        CREATE INDEX IF NOT EXISTS "scrapedjob_last_seen_on" ON "scrapedjob" ("last_seen_on");
        CREATE UNIQUE INDEX IF NOT EXISTS "scrapedjob_url" ON "scrapedjob" ("url");
    ''').strip()


def test_make_schema_idempotent_raises():
    with pytest.raises(ValueError):
        make_schema_idempotent(dedent('''
            CREATE UNIQUE INDEX "scrapedjob_url" ON "scrapedjob" ("url");
            INSERT INTO "transaction" VALUES(175,'2021-09-01','donations',6);
        '''))


@pytest.mark.parametrize('row_from, row_to, expected', [
    (dict(), dict(), dict()),
    (dict(a=1, b=2, c=3), dict(a=1, b=2, c=3), dict()),
    (dict(a=None, b=None, c=3), dict(a=None, b=None, c=3), dict()),
    (dict(a=1, b=2, c=3), dict(a=1, b=None, c=3), dict(b=2)),
    (dict(a=None, b=None, c=3), dict(a=1, b=2, c=3), dict()),
    (dict(a=None, b=42, c=3, d=None), dict(a=1, b=None, c=3, d=None), dict(b=42)),
])
def test_get_row_updates(row_from, row_to, expected):
    assert get_row_updates(row_from, row_to) == expected


@pytest.mark.parametrize('row_from, row_to', [
    (dict(a=1, b=2, c=3), dict(a=1, b=42, c=3)),
])
def test_get_row_updates_raises_conflict(row_from, row_to):
    with pytest.raises(RuntimeError):
        get_row_updates(row_from, row_to)


@pytest.mark.parametrize('row_from, row_to', [
    (dict(a=1, b=2, c=3, d=4), dict(a=1, b=2, c=3)),
    (dict(a=1, b=2, c=3), dict(a=1, b=2, c=3, d=4)),
])
def test_get_row_updates_raises_inconsistence(row_from, row_to):
    with pytest.raises(ValueError):
        get_row_updates(row_from, row_to)


def test_merge_unique_lines(tmp_path):
    path_from = tmp_path / 'path_from.txt'
    path_from.write_text('a\nb\nc\n')
    path_to = tmp_path / 'path_to.txt'
    path_to.write_text('d\ne\na\nf\nb\n')
    merge_unique_lines(path_from, path_to)

    assert path_from.read_text() == 'a\nb\nc\n'
    assert path_to.read_text() == 'd\ne\na\nf\nb\nc\n'


def test_merge_unique_lines_gzip(tmp_path):
    path_from = tmp_path / 'path_from.txt.gz'
    with gzip.open(path_from, 'wt') as f_from:
        f_from.write('a\nb\nc\n')
    path_to = tmp_path / 'path_to.txt.gz'
    with gzip.open(path_to, 'wt') as f_to:
        f_to.write('d\ne\na\nf\nb\n')
    merge_unique_lines(path_from, path_to, open=gzip.open)

    with gzip.open(path_from, 'rt') as f_from:
        assert f_from.read() == 'a\nb\nc\n'
    with gzip.open(path_to, 'rt') as f_to:
        assert f_to.read() == 'd\ne\na\nf\nb\nc\n'


def test_count_lines(tmp_path):
    path = tmp_path / 'path.txt'
    path.write_text('a\nb\nc\n')

    assert count_lines(path) == 3


def test_count_lines_gzip(tmp_path):
    path = tmp_path / 'path.txt'
    with gzip.open(path, 'wt') as f:
        f.write('a\nb\nc\nd\n')

    assert count_lines(path, open=gzip.open) == 4


@pytest.mark.parametrize('path, expected', [
    ('persist-to-workspace/0/.scrapy/http_cache/remoteok/6b/6b0ef6dce04d86506412fbe8e08f417f108f8115/request_headers', True),
    ('persist-to-workspace/0/juniorguru/images/avatars-club/0b5f22a77c1f5510921c930b6cb8ccdb.png', False),
])
def test_is_scrapy_cache(path, expected):
    assert is_scrapy_cache(path) is expected


@pytest.mark.parametrize('path, expected', [
    ('persist-to-workspace/0/juniorguru/data/jobs/2023/06/30/jobscz.jsonl.gz', True),
    ('persist-to-workspace/0/juniorguru/images/avatars-club/0b5f22a77c1f5510921c930b6cb8ccdb.png', False),
])
def test_is_jobs_archive(path, expected):
    assert is_jobs_archive(path) is expected
