import filecmp
import itertools
import re
import shutil
from fnmatch import fnmatch
from pathlib import Path
from pprint import pformat
from sqlite3 import IntegrityError

import click
from sqlite_utils import Database
from sqlite_utils.db import NotFoundError, Table

from jg.coop.lib import loggers
from jg.coop.lib.cache import CACHE_DIR, close_cache


SNAPSHOT_FILE = ".persist-to-workspace-snapshot"

PERSIST_DIR = "persist-to-workspace"

SNAPSHOT_EXCLUDE = [
    ".git",
    "backups",
    "node_modules",
    "public",
    ".image_templates_cache",
    ".pytest_cache",
    ".vscode",
    ".venv",
    ".ruff_cache",
    SNAPSHOT_FILE,
    PERSIST_DIR,
]

PERSIST_EXCLUDE = ["*.pyc", "*.db-shm", "*.db-wal", ".DS_Store"]

LOAD_EXCLUDE = PERSIST_EXCLUDE

SCHEMA_TRANSFORMATIONS = {
    re.compile(r"^CREATE TABLE"): "CREATE TABLE IF NOT EXISTS",
    re.compile(r"^(CREATE( UNIQUE)? INDEX)"): r"\1 IF NOT EXISTS",
    re.compile(r"^CREATE TRIGGER"): "CREATE TRIGGER IF NOT EXISTS",
}

DIR_NOT_EMPTY_ERRNO = 39


logger = loggers.from_path(__file__)


class CommaSeparated(click.ParamType):
    name = "commaseparated"

    def convert(self, value, param, context):
        return [item.strip() for item in value.split(",")]


@click.group()
def main():
    pass


@main.command()
@click.option("--file", default=SNAPSHOT_FILE, type=click.File(mode="w"))
@click.option("--exclude", default=",".join(SNAPSHOT_EXCLUDE), type=CommaSeparated())
def snapshot(file, exclude):
    for path, mtime in take_snapshot(".", exclude=exclude):
        logger.debug(path)
        assert " = " not in str(path)
        file.write(f"{path} = {mtime}\n")


@main.command()
@click.argument("namespace")
@click.option("--persist-dir", default=PERSIST_DIR, type=click.Path(path_type=Path))
@click.option(
    "--persist-exclude", default=",".join(PERSIST_EXCLUDE), type=CommaSeparated()
)
@click.option("--snapshot-file", default=SNAPSHOT_FILE, type=click.File())
@click.option(
    "--snapshot-exclude", default=",".join(SNAPSHOT_EXCLUDE), type=CommaSeparated()
)
@click.option("--move/--no-move", default=False)
def persist(
    persist_dir, namespace, snapshot_file, snapshot_exclude, persist_exclude, move
):
    shutil.rmtree(persist_dir, ignore_errors=True)
    namespace_dir = persist_dir / namespace
    namespace_dir.mkdir(parents=True)
    snapshot = {
        Path(path): float(mtime)
        for path, mtime in (line.split(" = ") for line in snapshot_file)
    }
    for path, mtime in take_snapshot(".", exclude=snapshot_exclude):
        if any(fnmatch(path.name, pattern) for pattern in persist_exclude):
            logger.debug(f"Excluding {path}")
        elif path not in snapshot:
            logger["new"].info(path)
            persist_file(".", path, namespace_dir, move=move)
        elif mtime > snapshot[path]:
            logger["mod"].info(path)
            persist_file(".", path, namespace_dir, move=move)
    for path in (path for path in persist_dir.glob("**/*") if path.is_file()):
        logger.info(path)


@main.command()
@click.option("--persist-dir", default=PERSIST_DIR, type=click.Path(path_type=Path))
@click.option("--move/--no-move", default=False)
@click.option("--exclude", default=",".join(LOAD_EXCLUDE), type=CommaSeparated())
def load(persist_dir, move, exclude):
    for namespace_dir in persist_dir.iterdir():
        for path in (path for path in namespace_dir.glob("**/*") if path.is_file()):
            if any(fnmatch(path.name, pattern) for pattern in exclude):
                logger.debug(f"Excluding {path}")
            else:
                logger.info(f"Loading {path}")
                load_file(namespace_dir, path, ".", move=move)
    if move:
        shutil.rmtree(persist_dir)


def take_snapshot(dir, exclude=None):
    exclude = [
        (f"{pattern.rstrip('/')}/**/*" if Path(pattern).is_dir() else pattern)
        for pattern in (exclude or [])
    ]
    excluded = itertools.chain.from_iterable(
        Path(dir).glob(pattern) for pattern in exclude
    )
    included = Path(dir).glob("**/*")
    for path in set(included) - set(excluded):
        if path.is_file():
            yield path.relative_to(dir), path.stat().st_mtime


def persist_file(
    source_dir: Path, source_path: Path, persist_dir: Path, move: bool = False
):
    persist_path = persist_dir / source_path.relative_to(source_dir)
    persist_path.parent.mkdir(parents=True, exist_ok=True)
    if source_path.suffix == ".db":
        if source_path.is_relative_to(CACHE_DIR):
            close_cache()
        prepare_database_for_moving(source_path)
    (shutil.move if move else shutil.copy2)(source_path, persist_path)


def load_file(persist_dir, persist_path, source_dir, move=False):
    persist_size = persist_path.stat().st_size
    source_path = source_dir / persist_path.relative_to(persist_dir)
    source_path.parent.mkdir(parents=True, exist_ok=True)
    if source_path.exists():
        source_size = source_path.stat().st_size
        if filecmp.cmp(persist_path, source_path, shallow=False):
            logger.info(
                f"Keeping {source_path} ({source_size}b), it's equal to {persist_path} ({persist_size}b)"
            )
        else:
            if source_path.suffix == ".db":
                logger.info(
                    f"Merging {source_path} ({source_size}b)"
                    f" with {persist_path} ({persist_size}b)"
                )
                merge_databases(persist_path, source_path)
            else:
                logger.warning(
                    f"Overwriting {source_path} ({source_size}b)"
                    f" with {persist_path} ({persist_size}b)"
                )
                shutil.copy2(persist_path, source_path)
        if move:
            persist_path.unlink()
    else:
        logger.info(f"Adding {source_path} from {persist_path} ({persist_size}b)")
        (shutil.move if move else shutil.copy2)(persist_path, source_path)


def prepare_database_for_moving(path: Path):
    db = Database(path)
    db.disable_wal()
    db.vacuum()


def merge_databases(path_from: Path, path_to: Path):
    # Would be awesome to use this:
    # - https://til.simonwillison.net/sqlite/cr-sqlite-macos
    # - https://github.com/vlcn-io/cr-sqlite
    logger["db"].info(f"Merging {path_from} to {path_to}")
    db_from, db_to = Database(path_from), Database(path_to)

    logger["db"].info("Applying schema")
    db_to.executescript(make_schema_idempotent(db_from.schema))

    for table_from in db_from.tables:
        name = table_from.name
        table_to = db_to[name]
        if not table_to.exists():
            raise RuntimeError(f"Table {name} should already exist!")
        logger["db"][name].info(
            f"Tables have {table_from.count} and {table_to.count} rows before merge"
        )

        if is_diskcache(table_from):
            logger["db"][name].info("Detected DiskCache")
            merge_diskcaches(table_from, table_to)
        elif is_diskcache_settings(table_from):
            logger["db"][name].info("Detected DiskCache settings")
            merge_diskcache_settings(table_from, table_to)
        else:
            merge_tables(table_from, table_to)
        logger["db"][name].info(f"Table has {table_to.count} rows after merge")

    # flush changes to disk, close all transactions
    db_to.close()

    # vacuum to shrink the file
    Database(path_to).vacuum()


def get_row_updates(row_from, row_to) -> dict:
    if frozenset(row_from.keys()) != frozenset(row_to.keys()):
        raise ValueError(
            f"Rows don't match! {list(row_from.keys())!r} ≠ {list(row_to.keys())!r}"
        )
    updates = {}
    for column_name, value_from in row_from.items():
        if value_from is not None:
            value_to = row_to[column_name]
            if value_to is None:
                updates[column_name] = value_from
            elif value_from != value_to:
                raise RuntimeError(
                    f"Conflict in column {column_name!r}! Values would be overwritten\n{pformat(row_from)}\n{pformat(row_to)}"
                )
    return updates


def merge_tables(table_from: Table, table_to: Table):
    logger_t = logger["db"][table_from.name]

    for row_from in table_from.rows:
        try:
            pks = [row_from[pk] for pk in table_from.pks]
        except KeyError:
            raise KeyError(
                f"Primary key {table_from.pks!r} not found in row:\n{pformat(row_from)}"
            )
        try:
            row_to = table_to.get(pks)
        except NotFoundError:
            logger_t.debug(f"Inserting {pks!r}")
            table_to.insert(row_from, pk=table_from.pks)
        else:
            try:
                updates = get_row_updates(row_from, row_to)
            except RuntimeError:
                logger_t.error(
                    "Conflicts found! This typically happens if two parallel scripts write values to the same column. Instead add a new column or a new 1:1 table"
                )
                raise
            if updates:
                logger_t.debug(f"Updating {pks!r} with {pformat(updates)}")
                table_to.update(pks, updates)


def is_diskcache(table: Table) -> bool:
    columns = frozenset(table.columns_dict.keys())
    return table.name == "Cache" and {"key", "raw", "filename", "value"} < columns


def merge_diskcaches(table_from: Table, table_to: Table):
    if not is_diskcache(table_from):
        raise ValueError(f"Table {table_from.name!r} (from) should be DiskCache!")
    if not is_diskcache(table_to):
        raise ValueError(f"Table {table_to.name!r} (to) should be DiskCache!")

    logger_t = logger["db"][table_from.name]

    for row_from in table_from.rows:
        row_from.pop("rowid")  # drop rowid and rely on unique key
        try:
            logger_t.debug(f"Inserting {row_from['key']!r}")
            table_to.insert(row_from)
        except IntegrityError:
            logger_t.debug(f"Row {row_from['key']!r} exists, updating")
            row_to = next(table_to.rows_where("key = ?", [row_from["key"]], limit=1))
            pks = [row_to[pk] for pk in table_to.pks]
            updates = dict(
                store_time=skip_none_max(
                    row_from["store_time"],
                    row_to["store_time"],
                ),
                expire_time=skip_none_max(
                    row_from["expire_time"],
                    row_to["expire_time"],
                ),
                access_time=skip_none_max(
                    row_from["access_time"],
                    row_to["access_time"],
                ),
                access_count=row_from["access_count"] + row_to["access_count"],
            )
            if row_from["store_time"] > row_to["store_time"]:
                updates |= dict(
                    tag=row_from["tag"],
                    size=row_from["size"],
                    mode=row_from["mode"],
                    filename=row_from["filename"],
                    value=row_from["value"],
                )
            logger_t.debug(f"Updating {pks!r} with {pformat(updates)}")
            table_to.update(pks, updates)


def is_diskcache_settings(table: Table) -> bool:
    return (
        table.name == "Settings"
        and table.use_rowid
        and list(table.columns_dict.keys()) == ["key", "value"]
    )


def merge_diskcache_settings(table_from: Table, table_to: Table) -> None:
    if not is_diskcache_settings(table_from):
        raise ValueError(
            f"Table {table_from.name!r} (from) should be DiskCache settings!"
        )
    if not is_diskcache_settings(table_to):
        raise ValueError(f"Table {table_to.name!r} (to) should be DiskCache settings!")

    logger_t = logger["db"][table_from.name]

    from_settings = {row["key"]: row["value"] for row in table_from.rows}
    to_settings = {row["key"]: row["value"] for row in table_to.rows}

    if from_settings == to_settings:
        logger_t.debug("Tables are equal, nothing to do")
        return

    if not from_settings:
        raise ValueError("DiskCache Settings table is empty!")

    for key, from_value in from_settings.items():
        to_value = to_settings.get(key)
        if to_value is None:
            logger_t.debug(f"Adding {key!r}")
            table_to.insert({"key": key, "value": from_value})
        elif to_value != from_value:
            logger_t.debug(f"Deleting {key!r}, {from_value!r} ≠ {to_value!r}")
            table_to.delete_where("key = ?", [key])


def make_schema_idempotent(schema) -> str:
    return "\n".join(
        map(make_schema_line_idempotent, filter(None, schema.splitlines()))
    )


def make_schema_line_idempotent(schema_line) -> str:
    for transformation_re, replacement in SCHEMA_TRANSFORMATIONS.items():
        if transformation_re.search(schema_line):
            return transformation_re.sub(replacement, schema_line)
    raise ValueError(f"Unexpected schema line: {schema_line!r}")


def skip_none_max(*values):
    values = list(filter(None, values))
    if len(values) == 1:
        return values[0]
    if values:
        return max(values)
    return None
