import re
from pathlib import Path
import shutil
import itertools
from fnmatch import fnmatch
import filecmp
from pprint import pformat

from sqlite_utils import Database
from sqlite_utils.db import NotFoundError
import click

from juniorguru.lib import loggers


SNAPSHOT_FILE = '.persist-to-workspace-snapshot'

PERSIST_DIR = 'persist-to-workspace'

SNAPSHOT_EXCLUDE = [
    '.git',
    'backups',
    'node_modules',
    'public',
    SNAPSHOT_FILE,
    PERSIST_DIR,
]

PERSIST_EXCLUDE = ['*.pyc', '*.db-shm', '*.db-wal', '.DS_Store']

LOAD_EXCLUDE = PERSIST_EXCLUDE

SCHEMA_TRANSFORMATIONS = {
    re.compile(r'^CREATE TABLE'): 'CREATE TABLE IF NOT EXISTS',
    re.compile(r'^(CREATE( UNIQUE)? INDEX)'): r'\1 IF NOT EXISTS',
}

DIR_NOT_EMPTY_ERRNO = 39


logger = loggers.from_path(__file__)


class CommaSeparated(click.ParamType):
    name = 'commaseparated'
    def convert(self, value, param, context):
        return [item.strip() for item in value.split(',')]



@click.group()
def main():
    pass


@main.command()
@click.option('--file', default=SNAPSHOT_FILE, type=click.File(mode='w'))
@click.option('--exclude', default=','.join(SNAPSHOT_EXCLUDE), type=CommaSeparated())
def snapshot(file, exclude):
    for path, mtime in take_snapshot('.', exclude=exclude):
        logger.debug(path)
        assert ' = ' not in str(path)
        file.write(f"{path} = {mtime}\n")


@main.command()
@click.argument('namespace')
@click.option('--persist-dir', default=PERSIST_DIR, type=click.Path(path_type=Path))
@click.option('--persist-exclude', default=','.join(PERSIST_EXCLUDE), type=CommaSeparated())
@click.option('--snapshot-file', default=SNAPSHOT_FILE, type=click.File())
@click.option('--snapshot-exclude', default=','.join(SNAPSHOT_EXCLUDE), type=CommaSeparated())
@click.option('--move/--no-move', default=False)
def persist(persist_dir, namespace, snapshot_file, snapshot_exclude, persist_exclude, move):
    shutil.rmtree(persist_dir, ignore_errors=True)
    namespace_dir = persist_dir / namespace
    namespace_dir.mkdir(parents=True)
    snapshot = {Path(path): float(mtime)
                for path, mtime
                in (line.split(' = ') for line in snapshot_file)}
    for path, mtime in take_snapshot('.', exclude=snapshot_exclude):
        if any(fnmatch(path.name, pattern) for pattern in persist_exclude):
            logger.debug(f"Excluding {path}")
        elif path not in snapshot:
            logger['new'].info(path)
            persist_file('.', path, namespace_dir, move=move)
        elif mtime > snapshot[path]:
            logger['mod'].info(path)
            persist_file('.', path, namespace_dir, move=move)
    for path in (path for path in persist_dir.glob('**/*')
                 if path.is_file()):
        logger.info(path)


@main.command()
@click.option('--persist-dir', default=PERSIST_DIR, type=click.Path(path_type=Path))
@click.option('--move/--no-move', default=False)
@click.option('--exclude', default=','.join(LOAD_EXCLUDE), type=CommaSeparated())
def load(persist_dir, move, exclude):
    for namespace_dir in persist_dir.iterdir():
        for path in (path for path in namespace_dir.glob('**/*')
                    if path.is_file()):
            if any(fnmatch(path.name, pattern) for pattern in exclude):
                logger.debug(f"Excluding {path}")
            else:
                logger.info(path)
                load_file(namespace_dir, path, '.', move=move)
    if move:
        shutil.rmtree(persist_dir)


def take_snapshot(dir, exclude=None):
    exclude = [(f"{pattern.rstrip('/')}/**/*" if Path(pattern).is_dir() else pattern)
               for pattern in (exclude or [])]
    excluded = itertools.chain.from_iterable(Path(dir).glob(pattern)
                                             for pattern in exclude)
    included = Path(dir).glob('**/*')
    for path in set(included) - set(excluded):
        if path.is_file():
            yield path.relative_to(dir), path.stat().st_mtime


def persist_file(source_dir, source_path, persist_dir, move=False):
    persist_path = persist_dir / source_path.relative_to(source_dir)
    persist_path.parent.mkdir(parents=True, exist_ok=True)
    if source_path.suffix == '.db':
        prepare_database_for_moving(source_path)
    (shutil.move if move else shutil.copy2)(source_path, persist_path)


def load_file(persist_dir, persist_path, source_dir, move=False):
    source_path = source_dir / persist_path.relative_to(persist_dir)
    source_path.parent.mkdir(parents=True, exist_ok=True)
    if source_path.exists() and not filecmp.cmp(persist_path, source_path, shallow=False):
        if source_path.suffix == '.db':
            merge_databases(persist_path, source_path)
        else:
            raise RuntimeError(f"Conflict loading {persist_path}, file already exists: {source_path}")
        if move:
            persist_path.unlink()
    else:
        (shutil.move if move else shutil.copy2)(persist_path, source_path)


def prepare_database_for_moving(path):
    db = Database(path)
    db.disable_wal()
    db.vacuum()


def merge_databases(path_from, path_to):
    logger_db = logger['db']
    logger_db.info(f"Merging {path_from} to {path_to}")
    db_from, db_to = Database(path_from), Database(path_to)

    logger_db.info("Applying schema")
    db_to.executescript(make_schema_idempotent(db_from.schema))

    for table_from in db_from.tables:
        name = table_from.name
        logger_t = logger_db[name]
        table_to = db_to[name]

        if not table_to.exists():
            raise RuntimeError(f"Table {name} should already exist!")
        logger_t.info(f"Table has {table_to.count} rows, merging {table_from.count} rows")

        for row_from in table_from.rows:
            pks = [row_from[pk] for pk in table_from.pks]
            try:
                row_to = table_to.get(pks)
            except NotFoundError:
                logger_t.debug(f"Inserting {pks!r}")
                table_to.insert(row_from, pk=table_from.pks)
            else:
                try:
                    updates = get_row_updates(row_from, row_to)
                except RuntimeError:
                    logger_t.error("Conflicts found! This typically happens if two parallel scripts write values to the same column. Instead add a new column or a new 1:1 table")
                    raise
                if updates:
                    logger_t.debug(f"Updating {pks!r} with {pformat(updates)}")
                    table_to.update(pks, updates)
        logger_t.info(f"Table has {table_to.count} rows after merge")
    db_to.vacuum()


def get_row_updates(row_from, row_to):
    if frozenset(row_from.keys()) != frozenset(row_to.keys()):
        raise ValueError(f"Rows don't match! {list(row_from.keys())!r} ≠ {list(row_to.keys())!r}")
    updates = {}
    for column_name, value_from in row_from.items():
        value_to = row_to[column_name]
        if value_from is not None and value_to is None:
            updates[column_name] = value_from
        elif value_from != value_to:
            raise RuntimeError(f"Conflict in column {column_name}! Values would be overwritten")
    return updates


def make_schema_idempotent(schema):
    return '\n'.join(map(make_schema_line_idempotent, filter(None, schema.splitlines())))


def make_schema_line_idempotent(schema_line):
    for transformation_re, replacement in SCHEMA_TRANSFORMATIONS.items():
        if transformation_re.search(schema_line):
            return transformation_re.sub(replacement, schema_line)
    raise ValueError(f"Unexpected schema line: {schema_line!r}")
