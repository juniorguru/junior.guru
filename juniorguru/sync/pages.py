from pprint import pformat
from typing import Any

from mkdocs.config import load_config
from mkdocs.structure.files import get_files
from mkdocs.utils import meta

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.models.base import db
from juniorguru.models.page import Page
from juniorguru.web.templates import TEMPLATES


logger = loggers.from_path(__file__)


# See 'Generating pages from templates' on why the dependencies are needed
@cli.sync_command(dependencies=['course-providers', 'partners', 'events', 'podcast'])
@db.connection_context()
def main():
    logger.info('Setting up db table')
    Page.drop_table()
    Page.create_table()

    logger.info('Reading Markdown source files')
    config = load_config(config_file='juniorguru/web/mkdocs.yml')
    files = get_files(config)
    for file in files.documentation_pages():
        logger.debug(f"Reading: {file.src_uri}")
        with open(file.abs_src_path, encoding='utf-8-sig', errors='strict') as f:
            source = f.read()
        meta_data = parse_meta(source)
        data = dict(src_uri=file.src_uri,
                    dest_uri=file.dest_uri,
                    size=len(source),
                    meta=meta_data,
                    notes=parse_notes(source),
                    date=meta_data['date'] if 'date' in meta_data else None)
        logger.debug(f"Saving:\n{pformat(data)}")
        if not data['meta'].get('title'):
            raise ValueError(f"Page {file.src_uri} is missing a title")
        Page.create(**data)

    logger.info('Generating pages from templates')
    for _, generate_pages in TEMPLATES.items():
        for page in generate_pages():
            logger.debug(f"Reading: {page['path']}")
            data = dict(src_uri=page['path'],
                        dest_uri=page['path'].replace('.md', '/index.html'),
                        meta=page['meta'])
            logger.debug(f"Saving:\n{pformat(data)}")
            Page.create(**data)

    logger.info(f'Created {Page.select().count()} pages')


def parse_meta(source) -> dict[str, Any]:
    return meta.get_data(source.strip())[1]


def parse_notes(source) -> str:
    source = source.strip()
    parts = source.split('<!-- {#')
    if len(parts) == 1:
        return None
    if len(parts) > 2:
        raise ValueError("More than one block of notes")
    return parts[1].strip().removesuffix('#} -->').strip() or None
