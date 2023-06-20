import mimetypes
import pickle
import re
import shutil
import tempfile
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from subprocess import DEVNULL, PIPE, run

from jinja2 import Environment, FileSystemLoader
from PIL import Image
from playwright.sync_api import sync_playwright

from juniorguru.lib import loggers


NODE_MODULES_DIR = Path('node_modules')

FONTS = [NODE_MODULES_DIR / '@fontsource' / 'inter' / 'files',
         NODE_MODULES_DIR / 'bootstrap-icons' / 'font' / 'fonts']

CSS_REWRITE = [
    (r'(\.+/)+([^\.]+/)?([^\.]+\.woff)', r'./fonts/\3'),
]

IMAGES_DIR = Path('juniorguru/images')

TEMPLATES_DIR = Path('juniorguru/image_templates')


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


def render_template(width, height, template_name, context, filters=None):
    environment = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    environment.filters.update(filters or {})
    template = environment.get_template(template_name)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        logger.info(f'Rendering {width}x{height} {template_name} in {temp_dir}')

        html = template.render(images_dir=IMAGES_DIR.absolute(), **context)
        html_path = temp_dir / template_name
        html_path.write_text(html)

        logger.info('Compiling SCSS')
        run(['npx', 'sass', f'{TEMPLATES_DIR}:{temp_dir}'], check=True, stdout=DEVNULL)

        logger.info(f"Copying fonts: {', '.join(map(str, FONTS))}")
        fonts_dir = temp_dir / 'fonts'
        fonts_dir.mkdir(parents=True)
        for font_parent_dir in FONTS:
            for woff_path in Path(font_parent_dir).glob('**/*.woff*'):
                logger['font'].debug(f"Copying {woff_path} to {fonts_dir}")
                shutil.copy2(woff_path, fonts_dir)

        logger.info('Rewriting CSS')
        for css_path in temp_dir.glob('**/*.css'):
            logger['css'].debug(f"Rewriting {css_path}")
            for re_pattern, re_repl in CSS_REWRITE:
                css = css_path.read_text()
                rewritten_css = re.sub(re_pattern, re_repl, css)
                logger['css'].debug(f"Did pattern {re_pattern!r} result in changes? {(css != rewritten_css)}")
                css_path.write_text(rewritten_css)

        logger.info('Taking a screenshot')
        logger['screenshot'].debug(f"Taking screenshot {width}x{height} {html_path}")
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
        logger['screenshot'].debug('Editing screenshot')
        with Image.open(BytesIO(image_bytes)) as image:
            height_ar = (image.height * width) // image.width
            image = image.resize((width, height_ar), Image.Resampling.BICUBIC)
            image = image.crop((0, 0, width, height))

            edited_image_bytes = BytesIO()
            image.save(edited_image_bytes, 'PNG')
        logger['screenshot'].debug('Optimizing screenshot')
        edited_image_bytes.seek(0)
        proc = run(['npx', 'imagemin'], input=edited_image_bytes.getvalue(), stdout=PIPE, check=True)
        return proc.stdout
