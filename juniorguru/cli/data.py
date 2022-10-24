from pathlib import Path
import shutil
import itertools
from fnmatch import fnmatch
import sqlite3

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
    errors = False
    for namespace_dir in persist_dir.iterdir():
        for path in (path for path in namespace_dir.glob('**/*')
                     if path.is_file()):
            logger.info(path)
            try:
                load_file(namespace_dir, path, '.', move=move)
            except FileExistsError:
                errors = True
                logger.error(f"Exists: {path}")
            except NotImplementedError:
                errors = True
                logger.error(f"Not implemented: {path}")
    if errors:
        raise click.Abort()


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
        with sqlite3.connect(source_path) as db:
            persist_path = persist_path.with_suffix('.sql')
            with persist_path.open(mode='w') as f:
                for line in db.iterdump():
                    f.write(f"{line}\n")
    else:
        (shutil.move if move else shutil.copy2)(source_path, persist_path)


def load_file(persist_dir, persist_path, source_dir, move=False):
    source_path = source_dir / persist_path.relative_to(persist_dir)
    source_path.parent.mkdir(parents=True, exist_ok=True)
    if source_path.exists():
        raise FileExistsError(source_path)
    if persist_path.suffix == '.sql':
        source_path = source_path.with_suffix('.db')
        with sqlite3.connect(source_path) as db:
            db.executescript(source_path.read_text())
            db.execute('VACUUM;')
    else:
        (shutil.move if move else shutil.copy2)(persist_path, source_path)


# def merge_databases(path_src, path_dst):
#     db_src = Database(path_src)
#     db_dst = Database(path_dst)
#     for table_name in db_src.table_names():
#         for row in db_src[table_name].rows:
#             db_dst[table_name].insert(row)
#     db_dst.vacuum()
