from pathlib import Path
import shutil

import click
from sqlite_utils import Database

from juniorguru.lib import loggers


logger = loggers.get(__name__)


@click.group()
def main():
    pass


@main.command()
@click.argument('nodes_dir')
@click.argument('id')
def node(nodes_dir, id):
    node_dir = Path(nodes_dir) / id
    node_dir.mkdir(parents=True)

    logger.info('Copying Scrapy files')
    shutil.copytree('.scrapy', node_dir / 'scrapy')

    logger.info('Copying data files')
    shutil.copytree('juniorguru/data', node_dir / 'data')

    logger.info('Copying images')
    shutil.copytree('juniorguru/images', node_dir / 'images')


@main.command()
@click.argument('nodes_dir')
def merge(nodes_dir):
    for node_dir in Path(nodes_dir).iterdir():
        logger_n = logger.getChild(f'nodes.{node_dir.name}')

        logger_n.info('Copying Scrapy files')
        node_scrapy_dir = (node_dir / 'scrapy')
        for src_path in node_scrapy_dir.glob('**/*'):
            if src_path.is_file():
                dst_path = Path('.scrapy') / src_path.relative_to(node_scrapy_dir)
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                logger_n.debug(dst_path)
                shutil.copy2(src_path, dst_path)

        logger_n.info('Copying data jobs files')
        node_jobs_dir = (node_dir / 'data' / 'jobs')
        for src_path in node_jobs_dir.glob('**/*'):
            if src_path.is_file():
                dst_path = Path('juniorguru/data/jobs') / src_path.relative_to(node_jobs_dir)
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                logger_n.debug(dst_path)
                shutil.copy2(src_path, dst_path)

        logger_n.info('Copying other data files')
        node_data_dir = (node_dir / 'data')
        for src_path in node_data_dir.iterdir():
            if src_path.suffix in ['', '.yml', '.db-shm', '.db-wal']:
                logger_n.warning(f'Skipping {src_path}')
            elif src_path.suffix in ['.txt']:
                dst_path = Path('juniorguru/data') / src_path.relative_to(node_data_dir)
                logger_n.debug(dst_path)
                shutil.copy2(src_path, dst_path)
            elif src_path.name == 'data.db':
                dst_path = Path('juniorguru/data/data.db')
                if dst_path.exists():
                    logger_n.info('Merging databases')
                    merge_databases(src_path, dst_path)
                else:
                    logger_n.debug(dst_path)
                    shutil.copy2(src_path, dst_path)
            else:
                raise ValueError(f'Unexpected file! {src_path}')

        logger_n.info('Copying images')
        node_images_dir = (node_dir / 'images')
        for src_path in node_images_dir.glob('**/*'):
            if src_path.is_file():
                dst_path = Path('juniorguru/images') / src_path.relative_to(node_images_dir)
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                logger_n.debug(dst_path)
                shutil.copy2(src_path, dst_path)


def merge_databases(path_src, path_dst):
    db_src = Database(path_src)
    db_dst = Database(path_dst)
    for table_name in db_src.table_names():
        for row in db_src[table_name].rows:
            db_dst[table_name].insert(row)
    db_dst.vacuum()
