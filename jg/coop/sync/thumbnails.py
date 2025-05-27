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


# Generating thumbnails for the legacy Flask app requires jobs data and events
@cli.sync_command(dependencies=["pages", "jobs-listing", "events"])
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

        # # all below can be deleted once Flask is gone
        # logger.info("Dealing with legacy pages")
        # LegacyThumbnail.drop_table()
        # LegacyThumbnail.create_table()

        # equivalents = {
        #     "/": "index.jinja",
        #     "/club/": "club.md",
        #     "/events/": "events.md",
        #     "/courses/": "courses.md",
        #     "/podcast/": "podcast.md",
        #     "/handbook/": "handbook/index.md",
        #     "/handbook/candidate/": "handbook/candidate.md",
        #     "/news/": "news.jinja",
        #     "/jobs/": "jobs.jinja",
        # }
        # for url, src_uri in equivalents.items():
        #     page = Page.get(Page.src_uri == src_uri)
        #     LegacyThumbnail.create(url=url, image_path=page.thumbnail_path)

        # default_image_path = render_image_file(
        #     width, height, "thumbnail_legacy.jinja", {}, output_path
        # )
        # for url in [
        #     "/404.html",
        #     "/press/",
        #     "/press/crisis/",
        #     "/press/handbook/",
        #     "/press/women/",
        # ]:
        #     LegacyThumbnail.create(
        #         url=url, image_path=default_image_path.relative_to(images_path)
        #     )

        # args = [
        #     (
        #         url,
        #         width,
        #         height,
        #         "thumbnail_legacy.jinja",
        #         dict(title=title),
        #         output_path,
        #     )
        #     for url, title in [
        #         ("/jobs/remote/", "Práce v IT pro začátečníky — na dálku"),
        #         ("/jobs/region/praha/", "Práce v IT pro začátečníky — Praha"),
        #         ("/jobs/region/brno/", "Práce v IT pro začátečníky — Brno"),
        #         ("/jobs/region/ostrava/", "Práce v IT pro začátečníky — Ostrava"),
        #         (
        #             "/jobs/region/ceske-budejovice/",
        #             "Práce v IT pro začátečníky — České Budějovice",
        #         ),
        #         (
        #             "/jobs/region/hradec-kralove/",
        #             "Práce v IT pro začátečníky — Hradec Králové",
        #         ),
        #         ("/jobs/region/jihlava/", "Práce v IT pro začátečníky — Jihlava"),
        #         (
        #             "/jobs/region/karlovy-vary/",
        #             "Práce v IT pro začátečníky — Karlovy Vary",
        #         ),
        #         ("/jobs/region/liberec/", "Práce v IT pro začátečníky — Liberec"),
        #         ("/jobs/region/olomouc/", "Práce v IT pro začátečníky — Olomouc"),
        #         ("/jobs/region/pardubice/", "Práce v IT pro začátečníky — Pardubice"),
        #         ("/jobs/region/plzen/", "Práce v IT pro začátečníky — Plzeň"),
        #         (
        #             "/jobs/region/usti-nad-labem/",
        #             "Práce v IT pro začátečníky — Ústí nad Labem",
        #         ),
        #         ("/jobs/region/zlin/", "Práce v IT pro začátečníky — Zlín"),
        #         ("/jobs/region/germany/", "Práce v IT pro začátečníky — Německo"),
        #         ("/jobs/region/poland/", "Práce v IT pro začátečníky — Polsko"),
        #         ("/jobs/region/austria/", "Práce v IT pro začátečníky — Rakousko"),
        #         ("/jobs/region/slovakia/", "Práce v IT pro začátečníky — Slovensko"),
        #     ]
        # ]
        # for url, image_path in pool.imap_unordered(process_thumbnail, args):
        #     LegacyThumbnail.create(
        #         url=url, image_path=image_path.relative_to(images_path)
        #     )

        # args = []
        # for _, params in generate_job_pages():
        #     job = ListedJob.get_by_submitted_id(params["job_id"])
        #     context = dict(
        #         job_title=job.title,
        #         job_company=job.company_name,
        #         job_location=job.location,
        #     )
        #     args.append(
        #         (
        #             f"/jobs/{params['job_id']}/",
        #             width,
        #             height,
        #             "thumbnail_legacy.jinja",
        #             context,
        #             output_path,
        #         )
        #     )
        # for url, image_path in pool.imap_unordered(process_thumbnail, args):
        #     LegacyThumbnail.create(
        #         url=url, image_path=image_path.relative_to(images_path)
        #     )

        # expected_urls = frozenset(get_freezer(app).all_urls())
        # urls = frozenset(thumbnail.url for thumbnail in LegacyThumbnail.select())
        # missing_urls = expected_urls - urls
        # if missing_urls:
        #     logger.error(f"Missing legacy pages: {', '.join(sorted(missing_urls))}")
        #     raise click.Abort()


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
