from pathlib import Path
from textwrap import dedent

import pytest
from sqlite_utils import Database

from jg.coop.cli.data import get_row_updates, make_schema_idempotent, merge_databases


def test_make_schema_idempotent():
    assert (
        make_schema_idempotent(
            dedent(
                """
        CREATE TABLE "clubdocumentedrole" ("id" INTEGER NOT NULL PRIMARY KEY, "name" VARCHAR(255) NOT NULL, "mention" VARCHAR(255) NOT NULL, "slug" VARCHAR(255) NOT NULL, "description" TEXT NOT NULL, "position" INTEGER NOT NULL, "emoji" VARCHAR(255));
        CREATE TABLE "clubpinreaction" ("id" INTEGER NOT NULL PRIMARY KEY, "user_id" INTEGER NOT NULL, "message_id" INTEGER NOT NULL, FOREIGN KEY ("user_id") REFERENCES "clubuser" ("id"), FOREIGN KEY ("message_id") REFERENCES "clubmessage" ("id"));
        CREATE INDEX "scrapedjob_last_seen_on" ON "scrapedjob" ("last_seen_on");
        CREATE UNIQUE INDEX "scrapedjob_url" ON "scrapedjob" ("url");
    """
            )
        ).strip()
        == dedent(
            """
        CREATE TABLE IF NOT EXISTS "clubdocumentedrole" ("id" INTEGER NOT NULL PRIMARY KEY, "name" VARCHAR(255) NOT NULL, "mention" VARCHAR(255) NOT NULL, "slug" VARCHAR(255) NOT NULL, "description" TEXT NOT NULL, "position" INTEGER NOT NULL, "emoji" VARCHAR(255));
        CREATE TABLE IF NOT EXISTS "clubpinreaction" ("id" INTEGER NOT NULL PRIMARY KEY, "user_id" INTEGER NOT NULL, "message_id" INTEGER NOT NULL, FOREIGN KEY ("user_id") REFERENCES "clubuser" ("id"), FOREIGN KEY ("message_id") REFERENCES "clubmessage" ("id"));
        CREATE INDEX IF NOT EXISTS "scrapedjob_last_seen_on" ON "scrapedjob" ("last_seen_on");
        CREATE UNIQUE INDEX IF NOT EXISTS "scrapedjob_url" ON "scrapedjob" ("url");
    """
        ).strip()
    )


def test_make_schema_idempotent_raises():
    with pytest.raises(ValueError):
        make_schema_idempotent(
            dedent(
                """
            CREATE UNIQUE INDEX "scrapedjob_url" ON "scrapedjob" ("url");
            INSERT INTO "transaction" VALUES(175,'2021-09-01','donations',6);
        """
            )
        )


@pytest.mark.parametrize(
    "row_from, row_to, expected",
    [
        ({}, {}, {}),
        ({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 3}, {}),
        ({"a": None, "b": None, "c": 3}, {"a": None, "b": None, "c": 3}, {}),
        ({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": None, "c": 3}, {"b": 2}),
        ({"a": None, "b": None, "c": 3}, {"a": 1, "b": 2, "c": 3}, {}),
        (
            {"a": None, "b": 42, "c": 3, "d": None},
            {"a": 1, "b": None, "c": 3, "d": None},
            {"b": 42},
        ),
    ],
)
def test_get_row_updates(row_from, row_to, expected):
    assert get_row_updates(row_from, row_to) == expected


@pytest.mark.parametrize(
    "row_from, row_to",
    [
        ({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 42, "c": 3}),
    ],
)
def test_get_row_updates_raises_conflict(row_from, row_to):
    with pytest.raises(RuntimeError):
        get_row_updates(row_from, row_to)


@pytest.mark.parametrize(
    "row_from, row_to",
    [
        ({"a": 1, "b": 2, "c": 3, "d": 4}, {"a": 1, "b": 2, "c": 3}),
        ({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 3, "d": 4}),
    ],
)
def test_get_row_updates_raises_inconsistence(row_from, row_to):
    with pytest.raises(ValueError):
        get_row_updates(row_from, row_to)


def create_db(path: Path, rows: list[dict]) -> None:
    db = Database(path)
    db.execute(
        'CREATE TABLE "items" ("id" INTEGER NOT NULL PRIMARY KEY, "name" TEXT NOT NULL, "note" TEXT)'
    )
    db["items"].insert_all(rows)
    db.close()


def test_merge_databases(tmp_path: Path):
    path_from, path_to = tmp_path / "from.db", tmp_path / "to.db"
    create_db(
        path_from,
        [
            {"id": 1, "name": "same", "note": None},
            {"id": 2, "name": "filled", "note": "new"},
            {"id": 3, "name": "added", "note": None},
        ],
    )
    create_db(
        path_to,
        [
            {"id": 1, "name": "same", "note": None},
            {"id": 2, "name": "filled", "note": None},
            {"id": 4, "name": "kept", "note": None},
        ],
    )

    merge_databases(path_from, path_to)

    assert list(Database(path_to)["items"].rows_where(order_by="id")) == [
        {"id": 1, "name": "same", "note": None},
        {"id": 2, "name": "filled", "note": "new"},
        {"id": 3, "name": "added", "note": None},
        {"id": 4, "name": "kept", "note": None},
    ]


def test_merge_databases_raises_conflict(tmp_path: Path):
    path_from, path_to = tmp_path / "from.db", tmp_path / "to.db"
    create_db(path_from, [{"id": 1, "name": "a", "note": None}])
    create_db(path_to, [{"id": 1, "name": "b", "note": None}])

    with pytest.raises(RuntimeError):
        merge_databases(path_from, path_to)
