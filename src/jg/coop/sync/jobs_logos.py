import hashlib
import itertools
from datetime import timedelta
from io import BytesIO
from pathlib import Path

import click
import httpx
from PIL import Image, ImageChops, ImageOps
from pydantic import BaseModel

from jg.coop.cli.sync import main as cli
from jg.coop.lib import apify, loggers
from jg.coop.lib.cache import cache
from jg.coop.lib.images import create_fallback_image
from jg.coop.lib.mutations import MutationsNotAllowedError
from jg.coop.models.base import db
from jg.coop.models.job import ListedJob, LogoSourceType


SIZE_PX = 100

IMAGES_DIR = Path("src/jg/coop/images")

IMAGE_SAVE_OPTIONS = {"format": "WEBP", "optimize": True}

LOGOS_DIR = IMAGES_DIR / "logos-jobs"


logger = loggers.from_path(__file__)


class LogoImage(BaseModel):
    image_url: str
    original_image_url: str
    width: int
    height: int
    format: str
    source_url: str


class Logo(BaseModel):
    image: LogoImage
    source_type: LogoSourceType


@cache(expire=timedelta(days=14), tag="job-logos")
def fetch_logos(actor_name: str, urls: list[str]) -> list[dict]:
    return apify.run(actor_name, {"links": [{"url": url} for url in urls]})


@cli.sync_command(dependencies=["jobs-listing"])
@click.option("--actor", "actor_name", default="honzajavorek/job-logos")
@click.option("--clear-files/--keep-files", default=False)
@db.connection_context()
def main(actor_name: str, clear_files: bool):
    Path(LOGOS_DIR).mkdir(exist_ok=True, parents=True)
    jobs = list(ListedJob.listing())

    if clear_files:
        logger.info("Clearing existing logo files")
        for path in LOGOS_DIR.glob("*.webp"):
            path.unlink()
    for job in jobs:
        job.company_logo_path = None
        job.save()

    logger.info("Collecting logo URLs")
    source_urls = sorted(
        set(
            (
                url
                for url in itertools.chain.from_iterable(
                    job.company_logo_source_urls for job in jobs
                )
                if url.startswith(("http://", "https://"))
            )
        )
    )
    try:
        logger.info(f"Fetching {len(source_urls)} logo URLs")
        logo_images = logger.wait(fetch_logos, actor_name, source_urls)
    except MutationsNotAllowedError:
        logger.warning("Not allowed to fetch logos, relying on stale data")
        logo_images = apify.fetch_data(actor_name)
    logo_images = [LogoImage(**logo_image) for logo_image in logo_images]

    logger.info(f"Processing {len(logo_images)} logo images")
    for job in jobs:
        logger.debug(f"Processing job {job.url}")
        logos = []
        for logo_image in logo_images:
            if source_type := job.get_logo_source_type(logo_image.source_url):
                logos.append(Logo(image=logo_image, source_type=source_type))
        logos.sort(key=sort_key)
        logger.debug(f"Logo candidates: {len(logos)}")
        for logo in logos:
            logger.info(f"Source {logo.image.original_image_url}")
            basename = hashlib.sha256(logo.image.image_url.encode()).hexdigest()
            logo_path = LOGOS_DIR / f"{basename}.webp"
            logger.info(f"Destination {logo_path}")
            if logo_path.exists():
                logger.debug(f"Logo {logo_path} already exists, skipping download")
            else:
                logger.debug(f"Downloading: {logo.image.image_url}")
                response = httpx.get(logo.image.image_url, follow_redirects=True)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                convert_image(image).save(logo_path, **IMAGE_SAVE_OPTIONS)
            job.company_logo_path = logo_path.relative_to(IMAGES_DIR)
            job.save()
            break

    remaining_jobs = list(ListedJob.no_logo_listing())
    logger.info(
        f"Generating fallback logo images for {len(remaining_jobs)} remaining jobs"
    )
    for job in remaining_jobs:
        hash = hashlib.sha256(f"initial-{job.initial}".encode()).hexdigest()
        image_path = LOGOS_DIR / f"{hash}.webp"
        logger.info(f"Destination {image_path}")
        if image_path.exists():
            logger.debug(f"Path {image_path} already exists")
        else:
            logger.debug(f"Generating initial {job.initial!r}")
            image = create_fallback_image(job.initial, SIZE_PX)
            image.save(image_path, **IMAGE_SAVE_OPTIONS)
        job.company_logo_path = image_path.relative_to(IMAGES_DIR)
        job.save()
        logger.debug(f"Logo for {job!r}: {job.company_logo_path}")

    logger.info("Generating special question mark logo for club jobs")
    create_fallback_image("?", SIZE_PX).save(
        LOGOS_DIR / "unknown.webp", **IMAGE_SAVE_OPTIONS
    )


def sort_key(logo: Logo) -> tuple[bool, int, int]:
    # Prioritize logos over icons (True sorts after False)
    is_icon = logo.source_type == LogoSourceType.ICON

    # Closer to zero, more like square. For small images, the shape doesn't
    # matter. All will be compared as if they were perfect squares.
    if logo.image.width < SIZE_PX or logo.image.height < SIZE_PX:
        similarity_to_square = 0
    else:
        similarity_to_square = abs(logo.image.width - logo.image.height)

    # Multiplied by -1 to ensure descending sort, i.e. larger is better.
    area = -1 * logo.image.width * logo.image.height

    return (is_icon, similarity_to_square, area)


def convert_image(image: Image) -> Image:
    # transparent to white
    image = image.convert("RGBA")
    background = Image.new("RGBA", image.size, (255, 255, 255))
    background.paste(image, (0, 0), image)
    image = background.convert("RGB")

    # trim white
    background = Image.new("RGB", image.size, (255, 255, 255))
    diff = ImageChops.difference(image, background)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    image = image.crop(diff.getbbox())

    # make it a square
    side_size = max(image.width, image.height)
    image = ImageOps.pad(image, (side_size, side_size), color=(255, 255, 255))

    # resize
    image = image.resize((SIZE_PX, SIZE_PX))

    return image
