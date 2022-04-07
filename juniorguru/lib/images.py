import os
import pickle
import tempfile
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from subprocess import DEVNULL, run

from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageOps


IMAGES_DIR = Path(__file__).parent.parent / 'images'
TEMPLATES_DIR = Path(__file__).parent.parent / 'image_templates'


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
    html = template.render(templates_dir=TEMPLATES_DIR, images_dir=IMAGES_DIR, **context)

    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        f.write(html.encode('utf-8'))
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # pageres doesn't support changing the output directory, so we need
            # to set cwd. The problem is, with cwd set to temp dir, npx stops
            # to work, therefore we need to use an explicit path here
            pageres = ['node', f'{os.getcwd()}/node_modules/.bin/pageres']
            run(pageres + [f'file://{f.name}', f'{width}x{height}',
                '--format=png', '--overwrite', '--filename=image'],
                cwd=temp_dir, check=True, stdout=DEVNULL)

            with Image.open(Path(temp_dir) / 'image.png') as image:
                buffer = BytesIO()
                image = image.crop((0, 0, width, height))
                image.save(buffer, 'PNG')
                return buffer.getvalue()
    finally:
        os.unlink(f.name)
