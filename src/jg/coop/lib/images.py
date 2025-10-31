import json
import mimetypes
import os
import pickle
import shutil
import time
from functools import lru_cache
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from subprocess import run
from typing import Any, Callable, Generator, Iterable

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

from jg.coop.lib import loggers
from jg.coop.lib.cache import get_cache, get_jinja_cache


CACHE_DIR = Path(".image_templates_cache")

IMAGES_DIR = Path("src/jg/coop/images")

TEMPLATES_DIR = Path("src/jg/coop/image_templates")

FONT_DIR = Path("node_modules/@fontsource/inter/files")

FONT_WIDTH = 800

FONT_PATHS = [
    FONT_DIR / f"inter-latin-{FONT_WIDTH}-normal.woff2",
    FONT_DIR / f"inter-latin-ext-{FONT_WIDTH}-normal.woff2",
]


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
    width: int,
    height: int,
    template_name: str,
    context: dict[str, Any],
    output_dir: Path | str,
    filters: dict[str, Callable] | None = None,
    prefix: str | None = None,
) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    cache_key = (width, height, template_name, context)
    hash = sha256(pickle.dumps(cache_key)).hexdigest()

    image_name = "-".join(filter(None, [prefix, hash])) + ".png"
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


def init_templates_cache(
    cache_dir: str | Path | None = None, cache_key: str = "image-templates-cache"
):
    cache = get_cache()
    cache_dir = Path(cache_dir or CACHE_DIR).absolute()

    if cache_dir.exists() and (prev_sources := cache.get(cache_key)):
        sources = dict(_get_fs_snapshot(prev_sources.keys()))
        if sources == prev_sources:
            logger.debug(f"Cache already initialized: {cache_dir}")
            return

    t = time.perf_counter()

    logger.debug(f"Removing cache: {cache_dir}")
    shutil.rmtree(cache_dir, ignore_errors=True)

    cache_dir.mkdir()
    logger.debug(f"Cache created: {cache_dir}")

    logger.debug("Building static assets")
    command = ["node", "esbuild-image-templates.js", str(cache_dir)]
    result = run(command, check=True, capture_output=True, text=True)
    if stderr := result.stderr.strip():
        logger.warning(
            f"Running `{' '.join(command)}` produced {len(stderr)} stderr characters"
        )

    logger.debug("Reading esbuild metafile")
    source_paths = _get_source_paths(json.loads(result.stdout))
    sources = dict(_get_fs_snapshot(source_paths))
    cache.set(cache_key, sources)

    logger.info(f"Initialized {cache_dir} in {time.perf_counter() - t:.2f}s")


def _get_source_paths(metafile: dict[str, Any]) -> list[str]:
    source_paths = set()
    for input_path, input_spec in metafile["inputs"].items():
        source_paths.add(input_path)
        for import_spec in input_spec["imports"]:
            source_paths.add(import_spec["path"])
    return sorted(
        path.split("?", 1)[0] for path in source_paths if not path.startswith("data:")
    )


def _get_fs_snapshot(
    paths: Iterable[str | Path],
) -> Generator[tuple[str, tuple[float, int]], None, None]:
    for path in paths:
        try:
            stat = Path(path).stat()
        except FileNotFoundError:
            continue
        yield path, (stat.st_mtime, stat.st_size)


class PostersCache:
    def __init__(self, posters_dir: str | Path):
        self.posters_dir = Path(posters_dir)
        self.existing_paths = set()
        self.generated_paths = set()

    def init(self, clear: bool = False):
        self.existing_paths = set(self.posters_dir.glob("*.png"))
        if clear:
            logger.warning("Removing all existing posters")
            for path in self.existing_paths:
                path.unlink()
            self.existing_paths = set(self.posters_dir.glob("*.png"))

    def record(self, path: Path):
        self.generated_paths.add(path)

    def cleanup(self):
        for path in self.existing_paths - self.generated_paths:
            logger.info(f"Removing {path}")
            path.unlink()


def create_fallback_image(
    initial: str,
    size_px: int,
    color: tuple[int] = (231, 231, 231),
    bg_color: tuple[int] = (255, 255, 255),
    padding: int = 5,
) -> Image:
    logger.debug(f"Creating fallback image for {initial}")
    # the fonts provided by @fontsource/inter are split into files according to
    # the character set they support, so we need to choose the right one based
    # on the initial character
    font_path = next(
        font_path
        for font_path in FONT_PATHS
        if any(ord(initial) in table.cmap for table in load_font_tables(font_path))
    )

    logger.debug(f"Using font {font_path} for {initial}")
    image = Image.new("RGB", (size_px, size_px), bg_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, size_px - (padding * 2))

    logger.debug(f"Centering text for {initial}")
    _, _, box_width, box_height = draw.textbbox(xy=(0, 0), text=initial, font=font)
    text_width, text_height = font.getmask(initial).size
    x_text = (size_px - text_width) / 2
    y_text = ((size_px - box_height) / 2) - ((box_height - text_height) / 2)
    draw.text((x_text, y_text), text=initial, font=font, fill=color)

    return image


@lru_cache
def load_font_tables(font_path: Path) -> list[CmapSubtable]:
    logger.info(f"Loading font tables from {font_path}")
    return TTFont(font_path)["cmap"].tables
