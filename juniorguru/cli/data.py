from pathlib import Path
import shutil
import itertools

import click
# from sqlite_utils import Database

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


logger = loggers.get(__name__)


class Exclude(click.ParamType):
    name = 'exclude'

    def convert(self, value, param, context):
        return [pattern.strip() for pattern in value.split(',')]



@click.group()
def main():
    pass


@main.command()
@click.option('--file', default=SNAPSHOT_FILE, type=click.File(mode='w'))
@click.option('--exclude', default=','.join(SNAPSHOT_EXCLUDE), type=Exclude())
def snapshot(file, exclude):
    for path, mtime in take_snapshot('.', exclude=exclude):
        logger.debug(path)
        assert ' = ' not in str(path)
        file.write(f"{path} = {mtime}\n")


@main.command()
@click.argument('namespace')
@click.option('--persist-dir', default=PERSIST_DIR, type=click.Path())
@click.option('--snapshot-file', default=SNAPSHOT_FILE, type=click.File())
@click.option('--snapshot-exclude', default=','.join(SNAPSHOT_EXCLUDE), type=Exclude())
def persist(persist_dir, namespace, snapshot_file, snapshot_exclude):
    persist_dir = Path(persist_dir) / namespace
    persist_dir.mkdir(parents=True)
    snapshot = {Path(path): float(mtime)
                for path, mtime
                in (line.split(' = ') for line in snapshot_file)}
    for path, mtime in take_snapshot('.', exclude=snapshot_exclude):
        if path not in snapshot:
            logger.info(f"New: {path}")
            persist_file('.', path, persist_dir)
        elif mtime > snapshot[path]:
            logger.info(f"Modified: {path}")
            persist_file('.', path, persist_dir)


# @main.command()
# @click.argument('nodes_dir')
# @click.argument('id')
# def node(nodes_dir, id):
#     node_dir = Path(nodes_dir) / id
#     node_dir.mkdir(parents=True)

#     logger.info('Copying Scrapy files')
#     shutil.copytree('.scrapy', node_dir / 'scrapy')

#     logger.info('Copying data files')
#     shutil.copytree('juniorguru/data', node_dir / 'data')

#     logger.info('Copying images')
#     shutil.copytree('juniorguru/images', node_dir / 'images')


# @main.command()
# @click.argument('nodes_dir')
# def merge(nodes_dir):
#     for node_dir in Path(nodes_dir).iterdir():
#         logger_n = logger.getChild(f'nodes.{node_dir.name}')

#         logger_n.info('Copying Scrapy files')
#         node_scrapy_dir = (node_dir / 'scrapy')
#         for src_path in node_scrapy_dir.glob('**/*'):
#             if src_path.is_file():
#                 dst_path = Path('.scrapy') / src_path.relative_to(node_scrapy_dir)
#                 dst_path.parent.mkdir(parents=True, exist_ok=True)
#                 logger_n.debug(dst_path)
#                 shutil.copy2(src_path, dst_path)

#         logger_n.info('Copying data jobs files')
#         node_jobs_dir = (node_dir / 'data' / 'jobs')
#         for src_path in node_jobs_dir.glob('**/*'):
#             if src_path.is_file():
#                 dst_path = Path('juniorguru/data/jobs') / src_path.relative_to(node_jobs_dir)
#                 dst_path.parent.mkdir(parents=True, exist_ok=True)
#                 logger_n.debug(dst_path)
#                 shutil.copy2(src_path, dst_path)

#         logger_n.info('Copying other data files')
#         node_data_dir = (node_dir / 'data')
#         for src_path in node_data_dir.iterdir():
#             if src_path.suffix in ['', '.yml', '.db-shm', '.db-wal']:
#                 logger_n.warning(f'Skipping {src_path}')
#             elif src_path.suffix in ['.txt']:
#                 dst_path = Path('juniorguru/data') / src_path.relative_to(node_data_dir)
#                 logger_n.debug(dst_path)
#                 shutil.copy2(src_path, dst_path)
#             elif src_path.name == 'data.db':
#                 dst_path = Path('juniorguru/data/data.db')
#                 if dst_path.exists():
#                     logger_n.info('Merging databases')
#                     merge_databases(src_path, dst_path)
#                 else:
#                     logger_n.debug(dst_path)
#                     shutil.copy2(src_path, dst_path)
#             else:
#                 raise ValueError(f'Unexpected file! {src_path}')

#         logger_n.info('Copying images')
#         node_images_dir = (node_dir / 'images')
#         for src_path in node_images_dir.glob('**/*'):
#             if src_path.is_file():
#                 dst_path = Path('juniorguru/images') / src_path.relative_to(node_images_dir)
#                 dst_path.parent.mkdir(parents=True, exist_ok=True)
#                 logger_n.debug(dst_path)
#                 shutil.copy2(src_path, dst_path)


# def merge_databases(path_src, path_dst):
#     db_src = Database(path_src)
#     db_dst = Database(path_dst)
#     for table_name in db_src.table_names():
#         for row in db_src[table_name].rows:
#             db_dst[table_name].insert(row)
#     db_dst.vacuum()


def persist_file(source_dir, source_path, persist_dir):
    persist_path = persist_dir / source_path.relative_to(source_dir)
    persist_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, persist_path)


def take_snapshot(dir, exclude=None):
    exclude = [(f"{pattern.rstrip('/')}/**/*" if Path(pattern).is_dir() else pattern)
               for pattern in (exclude or [])]
    excluded = itertools.chain.from_iterable(Path(dir).glob(pattern)
                                             for pattern in exclude)
    included = Path(dir).glob('**/*')
    for path in set(included) - set(excluded):
        if path.is_file():
            yield path.relative_to(dir), path.stat().st_mtime
