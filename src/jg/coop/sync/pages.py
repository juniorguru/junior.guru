from pprint import pformat
from typing import Any

from mkdocs.config import load_config
from mkdocs.structure.files import get_files
from mkdocs.structure.nav import Navigation, get_navigation
from mkdocs.utils import meta
from playhouse.shortcuts import model_to_dict

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers, mkdocs_jinja
from jg.coop.models.base import db
from jg.coop.models.page import Page
from jg.coop.models.stage import Stage


logger = loggers.from_path(__file__)


GENERATORS_DEPENDENCIES = [  # see generators.py
    "course-providers",
    "events",
    "jobs-listing",
    "podcast",
]


@cli.sync_command(dependencies=["stages"] + GENERATORS_DEPENDENCIES)
@db.connection_context()
def main():
    logger.info("Setting up db table")
    Page.drop_table()
    Page.create_table()

    logger.info("Reading Markdown source files")
    mkdocs_jinja.monkey_patch()
    config = load_config(config_file="src/jg/coop/web/mkdocs.yml", hooks=[])
    config = config.plugins.on_config(config)
    config.plugins.on_pre_build(config=config)
    files = get_files(config)
    files = config.plugins.on_files(files, config=config)
    nav = get_navigation(files, config)
    nav = config.plugins.on_nav(nav, config=config, files=files)

    for file in files.documentation_pages():
        logger.debug(f"Reading: {file.src_uri}")

        # Beware https://github.com/mkdocs/mkdocs/releases/tag/1.6.0,
        # it could happen that file.abs_src_path won't exist
        with open(file.abs_src_path, encoding="utf-8-sig", errors="strict") as f:
            source = f.read()
        meta_data = parse_meta(source)
        notes = parse_notes(source)

        if meta_data.get("template") == "redirect.html":
            logger.debug(f"Skipping: {file.src_uri} (redirect)")
            continue

        page = Page.from_meta(file.src_uri, file.dest_uri, meta_data)
        mainnav_name, nav_name = get_nav_names(page.src_uri, nav)
        page.mainnav_name = mainnav_name
        page.nav_name = nav_name
        page.nav_sort_key = get_nav_sort_key(file.src_uri, nav)
        page.size = len(source)
        page.notes_size = len(notes) if notes else 0

        # TODO this is M:N and should be a table with foreign keys
        stages = set(meta_data.get("stages", []))
        unknown_stages = stages - {stage.slug for stage in Stage.listing()}
        if unknown_stages:
            raise ValueError(f"Unknown stages: {','.join(unknown_stages)}")

        page.save()
        logger.debug(f"Saved: {pformat(model_to_dict(page))}")

    logger.info(f"Created {Page.select().count()} pages")


def parse_meta(source: str) -> dict[str, Any]:
    return meta.get_data(source.strip())[1]


def parse_notes(source: str) -> str:
    source = source.strip()
    parts = source.split("<!-- {#")
    if len(parts) == 1:
        return None
    if len(parts) > 2:
        raise ValueError("More than one block of notes")
    return parts[1].strip().removesuffix("#} -->").strip() or None


def get_nav_names(src_uri: str, nav: Navigation) -> tuple[str, str]:
    nav_item = [item for item in nav.pages if item.file.src_uri == src_uri][0]
    return (list(nav_item.ancestors)[-1].title, nav_item.title)


def get_nav_sort_key(src_uri: str, nav: Navigation) -> int | None:
    for sort_key, item in enumerate(nav.pages):
        if item.file.src_uri == src_uri:
            return sort_key
    return None
