import mimetypes
import os
import pickle
import shutil
import time
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from subprocess import run
from typing import Any, Callable

from jinja2 import Environment, FileSystemLoader
from PIL import Image
from playwright.sync_api import sync_playwright

from jg.coop.lib import loggers
from jg.coop.lib.cache import get_jinja_cache


CACHE_DIR = Path(".image_templates_cache")

IMAGES_DIR = Path("jg/coop/images")

TEMPLATES_DIR = Path("jg/coop/image_templates")


logger = loggers.from_path(__file__)


class InvalidImage(Exception):
    pass


def is_image(path):
    return path.is_file() and is_image_mimetype(mimetypes.guess_type(path)[0])


def is_image_mimetype(mimetype):
    return mimetype.startswith("image") if mimetype else False


def validate_image(path, format=None, max_width=None, max_height=None):
    with Image.open(path) as image:
        if max_width and image.width > max_width:
            raise InvalidImage(
                f"Image {path} is too large: width {image.width} > {max_width}"
            )
        if max_height and image.height > max_height:
            raise InvalidImage(
                f"Image {path} is too large: height {image.height} > {max_height}"
            )
        if format and image.format != format:
            raise InvalidImage(
                f"Image {path} has incorrect format: {image.format} ≠ {format}"
            )


def render_image_file(
    width,
    height,
    template_name,
    context,
    output_dir,
    filters=None,
    prefix=None,
    suffix=None,
):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    cache_key = (width, height, template_name, context)
    hash = sha256(pickle.dumps(cache_key)).hexdigest()

    image_name = "-".join(filter(None, [prefix, hash, suffix])) + ".png"
    image_path = output_dir / image_name

    if not image_path.exists():
        image_bytes = render_template(width, height, template_name, context, filters)
        image_path.write_bytes(image_bytes)
    return image_path


def render_template(
    width: int,
    height: int,
    template_name: str,
    context: dict[str, Any],
    filters: dict[str, Callable] = None,
) -> bytes:
    logger.info(f"Rendering {width}x{height} {template_name}")
    if not len(list(CACHE_DIR.glob("*.css"))):
        raise FileNotFoundError(
            f"Cache {CACHE_DIR.absolute()} does not exist, run init_templates_cache() before rendering"
        )
    t = time.perf_counter()

    environment = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        auto_reload=False,
        bytecode_cache=get_jinja_cache(),
    )
    environment.filters.update(filters or {})
    template = environment.get_template(template_name)

    logger.info("Jinja rendering")
    html = template.render(images_dir=IMAGES_DIR.absolute(), **context)
    html_path = (
        CACHE_DIR.absolute() / f"{os.getpid()}-{time.perf_counter_ns()}-{template_name}"
    )
    html_path.write_text(html)

    logger.info(f"Taking screenshot {width}x{height} {html_path}")
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        try:
            page = browser.new_page()
            page.set_viewport_size({"width": width, "height": height})
            page.goto(f"file://{html_path}", wait_until="networkidle")
            image_bytes = page.screenshot()
            page.close()
        finally:
            browser.close()
    # html_path.unlink()

    logger.info("Editing screenshot")
    with Image.open(BytesIO(image_bytes)) as image:
        height_ar = (image.height * width) // image.width
        image = image.resize((width, height_ar), Image.Resampling.BICUBIC)
        image = image.crop((0, 0, width, height))

        stream = BytesIO()
        image.save(stream, "PNG", optimize=True)
    image_bytes = stream.getvalue()

    logger.info(f"Rendered {template_name} in {time.perf_counter() - t:.2f}s")
    return image_bytes


def init_templates_cache(cache_dir=None):
    cache_dir = Path(cache_dir or CACHE_DIR).absolute()
    t = time.perf_counter()

    logger.debug(f"Removing cache: {cache_dir}")
    shutil.rmtree(cache_dir, ignore_errors=True)

    cache_dir.mkdir()
    logger.debug(f"Cache created: {cache_dir}")

    logger.debug("Building static assets")
    run(["node", "esbuild-image-templates.js", str(cache_dir)], check=True)

    logger.info(f"Initialized {cache_dir} in {time.perf_counter() - t:.2f}s")


class PostersCache:
    def __init__(self, posters_dir: str | Path):
        self.posters_dir = Path(posters_dir)
        self.existing_paths = set()
        self.generated_paths = set()

    def init(self, clear: bool = False):
        if clear:
            logger.warning("Removing all existing posters")
            for path in self.existing_paths:
                path.unlink()
        self.existing_paths.update(self.posters_dir.glob("*.png"))

    def record(self, path: Path):
        self.generated_paths.add(path)

    def cleanup(self):
        for path in self.existing_paths - self.generated_paths:
            logger.info(f"Removing {path}")
            path.unlink()
