import re
from pathlib import Path
import shutil
import itertools
from fnmatch import fnmatch

from sqlite_utils import Database
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

SCHEMA_TRANSFORMATIONS = {
    re.compile(r'^CREATE TABLE'): 'CREATE TABLE IF NOT EXISTS',
    re.compile(r'^(CREATE( UNIQUE)? INDEX)'): r'\1 IF NOT EXISTS',
}

DIR_NOT_EMPTY_ERRNO = 39


logger = loggers.get(__name__)


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
def load(persist_dir, move):
        for namespace_dir in persist_dir.iterdir():
            for path in (path for path in namespace_dir.glob('**/*')
                        if path.is_file()):
                logger.info(path)
                load_file(namespace_dir, path, '.', move=move)
        if move:
            leftovers = [persist_dir] + list(persist_dir.glob('**/*'))
            logger.info(f"Removing leftovers:\n{'\n'.join(leftovers)}")
            for leftover in sorted(leftovers, reverse=True):
                leftover.rmdir()


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
    if source_path.exists():
        if source_path.suffix == '.db':
            merge_databases(persist_path, source_path)
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

    for table in db_from.tables:
        if not db_to[table.name].exists():
            raise RuntimeError(f"Table {table.name} should already exist!")
        logger_db.info(f"Table {table.name} has {db_to[table.name].count} rows, merging {table.count} rows")
        pks = db_to[table.name].pks
        db_to[table.name].upsert_all(map(keep_non_null_values, table.rows), pk=pks)
        db_to[table.name].insert_all(table.rows, pk=pks, ignore=True)
        logger_db.info(f"Table {table.name} has {db_to[table.name].count} rows after merge")
    db_to.vacuum()


def keep_non_null_values(row):
    return {column_name: value for column_name, value in row.items()
            if value is not None}


def make_schema_idempotent(schema):
    return '\n'.join(map(make_schema_line_idempotent, schema.splitlines()))


def make_schema_line_idempotent(schema_line):
    for transformation_re, replacement in SCHEMA_TRANSFORMATIONS.items():
        if transformation_re.search(schema_line):
            return transformation_re.sub(replacement, schema_line)
    raise ValueError(f"Unexpected schema line: {schema_line}")
