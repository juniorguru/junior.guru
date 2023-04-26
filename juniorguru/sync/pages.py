from pathlib import Path

from mkdocs.config import load_config
from mkdocs.structure.files import get_files
from mkdocs.utils import meta

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.models.base import db
from juniorguru.models.page import Page


PACKAGE_DIR = Path('juniorguru')


logger = loggers.from_path(__file__)


@cli.sync_command()
@db.connection_context()
def main():
    logger.info('Setting up db table')
    Page.drop_table()
    Page.create_table()

    logger.info('Reading MkDocs files')
    config = load_config(config_file='juniorguru/mkdocs/mkdocs.yml')
    files = get_files(config)
    for file in files.documentation_pages():
        logger.debug(f"Reading: {file.src_uri}")
        with open(file.abs_src_path, encoding='utf-8-sig', errors='strict') as f:
            source = f.read()
        data = dict(src_uri=file.src_uri,
                    dest_uri=file.dest_uri,
                    meta=meta.get_data(source)[1])
        Page.create(**data)
    logger.info(f'Created {Page.select().count()} pages')
