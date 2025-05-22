import hashlib
from io import BytesIO
from multiprocessing import Pool
from pathlib import Path
from urllib.parse import urlparse

import favicon
import requests
from fontTools.ttLib import TTFont
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.job import ListedJob


MAX_SIZE_PX = 1000

SIZE_PX = 100

IMAGES_DIR = Path("jg/coop/images")

LOGOS_DIR = IMAGES_DIR / "logos-jobs"

FONT_DIR = Path("node_modules/@fontsource/inter/files")

FONT_WIDTH = 800

WORKERS = 4

# https://docs.python-requests.org/en/master/user/advanced/#timeouts
REQUEST_TIMEOUT = (3.05, 15)

# Just copy-paste of raw headers Firefox sends to a web page. None of it is
# intentionally set to a specific value with a specific meaning.
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8,cs;q=0.6,sk;q=0.4,es;q=0.2",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "Cache-Control": "max-age=0",
}

USER_AGENTS = {
    "startupjobs.cz": "JuniorGuruBot (+https://junior.guru)",
}


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["jobs-listing"])
@db.connection_context()
def main():
    jobs = ListedJob.listing()

    logger.info("Clear old logos")
    Path(LOGOS_DIR).mkdir(exist_ok=True, parents=True)
    for path in LOGOS_DIR.glob("*.png"):
        path.unlink()
    for job in jobs:
        job.company_logo_path = None
        job.save()

    with Pool(WORKERS) as pool:
        urls = {}

        logger.info("Registering company logo URLs")
        for job in jobs:
            for logo_url in job.company_logo_urls:
                urls.setdefault(logo_url, dict(type="logo", jobs=[]))
                urls[logo_url]["jobs"].append(job.id)

        logger.info("Fetching and registering company icon URLs")
        inputs = ((job.id, job.company_url) for job in jobs if job.company_url)
        results = pool.imap_unordered(fetch_icon_urls, inputs)
        for job_id, icon_urls in logger.progress(results, chunk_size=5):
            for icon_url in icon_urls:
                urls.setdefault(icon_url, dict(type="icon", jobs=[]))
                urls[icon_url]["jobs"].append(job_id)

        logger.info("Downloading images from both logo and icon URLs")
        results = pool.imap_unordered(download_image, urls.keys())
        for image_url, image_path, orig_width, orig_height in logger.progress(
            results, chunk_size=5
        ):
            urls[image_url]["image_path"] = image_path
            urls[image_url]["orig_width"] = orig_width
            urls[image_url]["orig_height"] = orig_height

        logger.info("Deciding which images to use")
        logo_paths = {}
        for logo in sorted(urls.values(), key=sort_key):
            for job_id in logo["jobs"]:
                logo_paths.setdefault(job_id, logo["image_path"])
        for job in jobs:
            logo_path = logo_paths.get(job.id)
            if logo_path:
                job.company_logo_path = Path(logo_path).relative_to(IMAGES_DIR)
                logger.debug(f"Logo for {job!r}: {job.company_logo_path}")
            job.save()

    remaining_jobs = list(ListedJob.no_logo_listing())
    logger.info(
        f"Generating fallback logo images for {len(remaining_jobs)} remaining jobs"
    )
    for job in remaining_jobs:
        hash = hashlib.sha1(f"initial-{job.initial}".encode()).hexdigest()
        image_path = LOGOS_DIR / f"{hash}.png"
        logger.info(f"Generating to {image_path}")
        if image_path.exists():
            logger.debug(f"Path {image_path} already exists")
        else:
            logger.debug(f"Generating initial {job.initial!r}")
            image = create_fallback_image(job.initial)
            image.save(image_path)
        job.company_logo_path = image_path.relative_to(IMAGES_DIR)
        job.save()
        logger.debug(f"Logo for {job!r}: {job.company_logo_path}")

    logger.info("Generating special question mark logo for club jobs")
    create_fallback_image("?").save(LOGOS_DIR / "unknown.png")


def sort_key(logo):
    # Such image didn't download, put it to the end of the list
    if logo["image_path"] is None:
        return (True, 100000, 0)

    # Prioritize logos over icons (True sorts after False)
    is_icon = logo["type"] == "icon"

    # Closer to zero, more like square. For small images, the shape doesn't
    # matter. All will be compared as if they were perfect squares.
    if logo["orig_width"] < SIZE_PX or logo["orig_height"] < SIZE_PX:
        similarity_to_square = 0
    else:
        similarity_to_square = abs(logo["orig_width"] - logo["orig_height"])

    # Multiplied by -1 to ensure descending sort, i.e. larger is better.
    area = -1 * logo["orig_width"] * logo["orig_height"]

    return (is_icon, similarity_to_square, area)


def fetch_icon_urls(args):
    logger_f = logger["fetch_icon_urls"]
    job_id, company_url = args
    logger_f.debug(f"Fetching icon URLs for <ListedJob: {job_id}>, {company_url}")
    try:
        icons = favicon.get(
            company_url, timeout=REQUEST_TIMEOUT, headers=DEFAULT_REQUEST_HEADERS
        )
        urls = unique(icon.url for icon in icons)
        logger_f.info(
            f"Icon URLs found for <ListedJob: {job_id}>, {company_url}: {urls!r}"
        )
        return job_id, urls
    except Exception:
        logger_f.exception(
            f"Fetching icon URLs for <ListedJob: {job_id}>, {company_url} failed"
        )
        return job_id, []


def download_image(image_url):
    logger_d = logger["download_image"]
    logger_d.debug(f"Downloading {image_url}")
    try:
        headers = dict(DEFAULT_REQUEST_HEADERS)
        headers["User-Agent"] = choose_user_agent(image_url)
        response = requests.get(image_url, timeout=REQUEST_TIMEOUT, headers=headers)
        response.raise_for_status()

        orig_image = Image.open(BytesIO(response.content))
        orig_width, orig_height = orig_image.size
        if orig_width > MAX_SIZE_PX or orig_height > MAX_SIZE_PX:
            raise ValueError(
                f"Image too large ({orig_width}x{orig_height} < {MAX_SIZE_PX}x{MAX_SIZE_PX})"
            )

        hash = hashlib.sha1(image_url.encode()).hexdigest()
        image_path = LOGOS_DIR / f"{hash}.png"
        convert_image(orig_image).save(image_path)
        logger_d.info(f"Downloaded {image_url} as {image_path}")

        return image_url, image_path, orig_width, orig_height
    except Exception:
        logger_d.exception(f"Unable to download {image_url}")
        return image_url, None, None, None


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


def create_fallback_image(
    initial: str,
    color: tuple[int] = (231, 231, 231),
    bg_color: tuple[int] = (255, 255, 255),
    padding: int = 5,
) -> Image:  # TODO log as debug once CI stops failing
    logger.info(f"Creating fallback image for {initial}")
    # the fonts provided by @fontsource/inter are split into files according to
    # the character set they support, so we need to choose the right one based
    # on the initial character
    font_path = next(
        font_path
        for font_path in [
            FONT_DIR / f"inter-latin-{FONT_WIDTH}-normal.woff2",
            FONT_DIR / f"inter-latin-ext-{FONT_WIDTH}-normal.woff2",
        ]
        if any(ord(initial) in table.cmap for table in TTFont(font_path)["cmap"].tables)
    )

    logger.info(f"Using font {font_path} for {initial}")
    image = Image.new("RGB", (SIZE_PX, SIZE_PX), bg_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, SIZE_PX - (padding * 2))

    logger.info(f"Centering text for {initial}")
    _, _, box_width, box_height = draw.textbbox(xy=(0, 0), text=initial, font=font)
    text_width, text_height = font.getmask(initial).size
    x_text = (SIZE_PX - text_width) / 2
    y_text = ((SIZE_PX - box_height) / 2) - ((box_height - text_height) / 2)
    draw.text((x_text, y_text), text=initial, font=font, fill=color)

    return image


def unique(iterable):
    return list(frozenset(item for item in iterable if item is not None))


def choose_user_agent(url):
    hostname = urlparse(url).hostname.lstrip("www.")
    return USER_AGENTS.get(hostname, DEFAULT_REQUEST_HEADERS["User-Agent"])
