from datetime import datetime
from multiprocessing import Pool
from pathlib import Path

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.images import render_image_file
from jg.coop.lib.template_filters import icon, local_time, weekday
from jg.coop.models.base import db
from jg.coop.models.page import Page


WORKERS = 4


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["pages"])
@click.option(
    "--images-path",
    default="jg/coop/images",
    type=click.Path(exists=True, path_type=Path),
)
@click.option("--output-dir", default="thumbnails", type=click.Path(path_type=Path))
@click.option("--width", default=1280, type=int)
@click.option("--height", default=720, type=int)
@click.option("--clear/--keep", default=False)
@db.connection_context()
def main(images_path, output_dir, width, height, clear):
    output_path = images_path / output_dir
    output_path.mkdir(exist_ok=True)

    if clear:
        existing_paths = list(output_path.glob("*.png"))
        logger.info(f"Removing {len(existing_paths)} existing thumbnails")
        for existing_path in existing_paths:
            existing_path.unlink()

    with Pool(WORKERS) as pool:
        pages = list(Page.listing())
        logger.info(f"Generating {len(pages)} thumbnails")
        args = []
        for i, page in enumerate(pages):
            context = get_thumbnail_context(page)
            args.append((i, width, height, "thumbnail.jinja", context, output_path))
        for i, image_path in pool.imap_unordered(process_thumbnail, args):
            page = pages[i]
            page.thumbnail_path = image_path.relative_to(images_path)
            page.save()
            logger.info(f"Page {page.src_uri}: {image_path}")


def process_thumbnail(args: tuple[int, int, int, str, dict, Path]) -> tuple[int, Path]:
    i, args = args[0], args[1:]
    image_path = render_image_file(
        *args, filters=dict(local_time=local_time, weekday=weekday, icon=icon)
    )
    return i, image_path


def get_thumbnail_context(page: Page) -> dict:
    default_button_icon = {
        "Klub": "chat",
        "Příručka": "journals",
        "Kurzy": "mortarboard",
        "Práce": "clipboard2-check",
        "Inspirace": "rocket-takeoff",
        "Info": "info-square",
    }.get(page.mainnav_name, "arrow-right-circle")
    return dict(
        title=page.meta.get("thumbnail_title", page.meta["title"]),
        image_path=page.meta.get("thumbnail_image_path", "chick-avatar.png"),
        date=(
            datetime.fromisoformat(page.meta["thumbnail_date"])
            if page.meta.get("thumbnail_date")
            else None
        ),
        subheading=page.meta.get(
            "thumbnail_subheading", f"junior.guru — {page.mainnav_name}"
        ),
        button_heading=page.meta.get("thumbnail_button_heading"),
        button_icon=(
            None
            if page.meta.get("thumbnail_button_heading")
            else (page.meta.get("thumbnail_button_icon", default_button_icon))
        ),
        button_link=page.meta.get(
            "thumbnail_button_link", f"junior.guru/{page.dest_uri.split('/')[0]}"
        ),
        platforms=page.meta.get("thumbnail_platforms", []),
    )
