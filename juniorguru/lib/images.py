import os
from io import BytesIO
import pickle
import tempfile
from hashlib import sha256
from pathlib import Path
from subprocess import DEVNULL, run

from PIL import Image, ImageOps
from jinja2 import Environment, FileSystemLoader


IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 630

IMAGES_DIR = Path(__file__).parent.parent / 'images'
TEMPLATES_DIR = Path(__file__).parent.parent / 'image_templates'
OVERWRITE_HTML_IMAGES = bool(int(os.getenv('OVERWRITE_HTML_IMAGES', 0)))


def html_to_png_path(template_name, context, output_dir, filters=None):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    hash = sha256(pickle.dumps(context)).hexdigest()
    image_path = output_dir / f'{hash}.png'

    if OVERWRITE_HTML_IMAGES or not image_path.exists():
        image_bytes = template_to_png_bytes(template_name, context, filters)
        image_path.write_bytes(image_bytes)
    return image_path


def save_png_as_square(png_path):
    # make it a square
    with Image.open(png_path) as image:
        side_size = max(image.width, image.height)
        image = ImageOps.pad(image, (side_size, side_size), color=(0, 0, 0))

        png_square_path = png_path.with_name(f"{png_path.stem}-square{png_path.suffix}")
        with png_square_path.open(mode='wb') as f:
            image.save(f, 'PNG')


def template_to_png_bytes(template_name, context, filters=None):
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
            run(pageres + [f'file://{f.name}', f'{IMAGE_WIDTH}x{IMAGE_HEIGHT}',
                '--format=png', '--overwrite', '--filename=image'],
                cwd=temp_dir, check=True, stdout=DEVNULL)

            with Image.open(Path(temp_dir) / 'image.png') as image:
                buffer = BytesIO()
                image = image.crop((0, 0, IMAGE_WIDTH, IMAGE_HEIGHT))
                image.save(buffer, 'PNG')
                return buffer.getvalue()
    finally:
        os.unlink(f.name)
