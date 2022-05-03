import re
import pickle
import tempfile
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from subprocess import DEVNULL, run
import mimetypes
import shutil

from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageOps

from juniorguru.lib import loggers


NODE_MODULES_DIR = Path(__file__).parent.parent.parent / 'node_modules'

FONTS = [NODE_MODULES_DIR / '@fontsource' / 'inter' / 'files',
         NODE_MODULES_DIR / 'bootstrap-icons' / 'font' / 'fonts']

CSS_REWRITE = [
    (r'\./files/([^\.]+/)?([^\.]+\.woff)', r'\./fonts/\2'),
]

IMAGES_DIR = Path(__file__).parent.parent / 'images'

TEMPLATES_DIR = Path(__file__).parent.parent / 'image_templates'


logger = loggers.get(__name__)


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


def save_as_square(path, prefix=None, suffix=None):
    cache_key = str(path.relative_to(IMAGES_DIR))
    hash = sha256(cache_key.encode('utf-8')).hexdigest()

    image_name = '-'.join(filter(None, [prefix, hash, suffix])) + '.png'
    image_path = path.with_name(image_name)

    if not image_path.exists():
        with Image.open(path) as image:
            side_px = max(image.width, image.height)
            image = ImageOps.pad(image, (side_px, side_px), color=(0, 0, 0))
            image.save(image_path, 'PNG')
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
        logger.info(f'Rendering {width}x{height} {template_name} in {temp_dir}')

        html = template.render(images_dir=IMAGES_DIR, **context)
        html_path = Path(temp_dir) / template_name
        html_path.write_text(html)

        logger.info('Compiling SCSS')
        run(['npx', 'sass', f'{TEMPLATES_DIR}:{temp_dir}'], check=True, stdout=DEVNULL)

        logger.info(f"Copying fonts: {', '.join(map(str, FONTS))}")
        fonts_dir = Path(temp_dir) / 'fonts'
        fonts_dir.mkdir(parents=True)
        for font_parent_dir in FONTS:
            for woff_path in Path(font_parent_dir).glob('**/*.woff*'):
                logger.debug(f"Copying font {woff_path} to {fonts_dir}")
                shutil.copy2(woff_path, fonts_dir)

        logger.info('Rewriting CSS')
        for css_path in Path(temp_dir).glob('**/*.css'):
            logger.debug(f"Rewriting {css_path}")
            for re_pattern, re_repl in CSS_REWRITE:
                css = css_path.read_text()
                rewritten_css = re.sub(re_pattern, re_repl, css)
                logger.debug(f"Did pattern {re_pattern!r} result in changes? {(css != rewritten_css)}")
                css_path.write_text(rewritten_css)

        logger.info('Making a screenshot')
        # pageres doesn't support changing the output directory, so we need
        # to set cwd. The problem is, with cwd set to temp dir, npx stops
        # to work, therefore we need to use an explicit path here
        pageres = ['node', f'{NODE_MODULES_DIR}/.bin/pageres']
        run(pageres + [f'file://{html_path}', f'{width}x{height}',
            '--format=png', '--overwrite', f'--filename={html_path.stem}'],
            cwd=temp_dir, check=True, stdout=DEVNULL)

        logger.info('Saving image')
        image_path = Path(temp_dir) / f'{html_path.stem}.png'
        logger.debug(f'Saving image as {image_path}')
        with Image.open(image_path) as image:
            buffer = BytesIO()
            image = image.crop((0, 0, width, height))
            image.save(buffer, 'PNG')
            return buffer.getvalue()
