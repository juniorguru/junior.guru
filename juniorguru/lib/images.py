import mimetypes
import os
import pickle
import re
import shutil
import time
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from subprocess import DEVNULL, run
from typing import Any, Callable

import oxipng
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from playwright.sync_api import sync_playwright

from juniorguru.lib import loggers


NODE_MODULES_DIR = Path('node_modules')

CACHE_DIR = Path('.images_templates_cache')

FONTS = [NODE_MODULES_DIR / '@fontsource' / 'inter' / 'files',
         NODE_MODULES_DIR / 'bootstrap-icons' / 'font' / 'fonts']

CSS_REWRITE = [
    (r'(\.+/)+([^\.]+/)?([^\.]+\.woff)', r'./fonts/\3'),
]

IMAGES_DIR = Path('juniorguru/images')

TEMPLATES_DIR = Path('juniorguru/image_templates')

OXIPNG_TIMEOUT_MS = 1000


logger = loggers.from_path(__file__)


class InvalidImage(Exception):
    pass


def is_image(path):
    return path.is_file() and is_image_mimetype(mimetypes.guess_type(path)[0])


def is_image_mimetype(mimetype):
    return mimetype.startswith('image') if mimetype else False


def validate_image(path, format=None, max_width=None, max_height=None):
    with Image.open(path) as image:
        if max_width and image.width > max_width:
            raise InvalidImage(f'Image {path} is too large: width {image.width} > {max_width}')
        if max_height and image.height > max_height:
            raise InvalidImage(f'Image {path} is too large: height {image.height} > {max_height}')
        if format and image.format != format:
            raise InvalidImage(f'Image {path} has incorrect format: {image.format} ≠ {format}')


def render_image_file(width, height, template_name, context, output_dir, filters=None, prefix=None, suffix=None):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    cache_key = (width, height, template_name, context)
    hash = sha256(pickle.dumps(cache_key)).hexdigest()

    image_name = '-'.join(filter(None, [prefix, hash, suffix])) + '.png'
    image_path = output_dir / image_name

    if not image_path.exists():
        image_bytes = render_template(width, height, template_name, context, filters)
        image_path.write_bytes(image_bytes)
    return image_path


def downsize_square_photo(path, side_px):
    with Image.open(path) as image:
        if image.width != image.height:
            raise ValueError(f"Image {path} must be square, but is {image.width}x{image.height}")
        if image.width > side_px:
            image = image.resize((side_px, side_px))
            image.save(path, image.format)
        return path


def replace_with_jpg(path):
    modified = False
    with Image.open(path) as image:
        if image.mode != 'RGB':
            modified = True
            image = image.convert('RGB')

        path_jpg = path.with_suffix('.jpg')
        if path != path_jpg:
            modified = True
            path.unlink()
            path = path_jpg

        if modified:
            image.save(path, 'JPEG')
    return path


def render_template(width: int,
                    height: int,
                    template_name: str,
                    context: dict[str, Any],
                    filters: dict[str, Callable]=None) -> bytes:
    logger.info(f'Rendering {width}x{height} {template_name}')
    t = time.perf_counter()

    environment = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    environment.filters.update(filters or {})
    template = environment.get_template(template_name)

    try:
        CACHE_DIR.mkdir()
    except FileExistsError:
        logger.info(f'Cache exists: {CACHE_DIR.absolute()}')
    else:
        logger.info(f'Cache created: {CACHE_DIR.absolute()}')

        logger.info('Compiling SCSS')
        run(['npx', 'sass', f'{TEMPLATES_DIR}:{CACHE_DIR}'], check=True, stdout=DEVNULL)

        logger.info(f"Copying fonts: {', '.join(map(str, FONTS))}")
        fonts_dir = CACHE_DIR / 'fonts'
        fonts_dir.mkdir(parents=True)
        for font_parent_dir in FONTS:
            for woff_path in Path(font_parent_dir).glob('**/*.woff*'):
                logger.debug(f"Copying {woff_path} to {fonts_dir}")
                shutil.copy2(woff_path, fonts_dir)

        logger.info('Rewriting CSS')
        for css_path in CACHE_DIR.glob('**/*.css'):
            logger.debug(f"Rewriting {css_path}")
            for re_pattern, re_repl in CSS_REWRITE:
                css = css_path.read_text()
                rewritten_css = re.sub(re_pattern, re_repl, css)
                logger.debug(f"Did pattern {re_pattern!r} result in changes? {(css != rewritten_css)}")
                css_path.write_text(rewritten_css)

    logger.info('Jinja2 rendering')
    html = template.render(images_dir=IMAGES_DIR.absolute(), **context)
    html_path = CACHE_DIR.absolute() / f'{os.getpid()}-{template_name}'
    html_path.write_text(html)

    logger.info(f"Taking screenshot {width}x{height} {html_path}")
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        try:
            page = browser.new_page()
            page.set_viewport_size({'width': width, 'height': height})
            page.goto(f'file://{html_path}', wait_until='networkidle')
            image_bytes = page.screenshot()
            page.close()
        finally:
            browser.close()

    logger.info('Editing screenshot')
    with Image.open(BytesIO(image_bytes)) as image:
        height_ar = (image.height * width) // image.width
        image = image.resize((width, height_ar), Image.Resampling.BICUBIC)
        image = image.crop((0, 0, width, height))

        stream = BytesIO()
        image.save(stream, 'PNG', optimize=True)
    image_bytes = stream.getvalue()

    logger.info('Optimizing screenshot')
    image_bytes = oxipng.optimize_from_memory(image_bytes,
                                              force=True,
                                              strip=oxipng.Headers.all(),
                                              timeout=OXIPNG_TIMEOUT_MS)

    logger.info(f'Rendered {template_name} in {time.perf_counter() - t:.2f}s')
    return image_bytes
