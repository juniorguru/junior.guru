import os
import pickle
import tempfile
from hashlib import sha256
from pathlib import Path
from subprocess import DEVNULL, run

from jinja2 import Template


STATIC_DIR = Path(__file__).parent / 'static'
THUMBNAILS_DIR = STATIC_DIR / 'images' / 'thumbnails'


def thumbnail(**context):
    THUMBNAILS_DIR.mkdir(exist_ok=True, parents=True)

    hash = sha256(pickle.dumps(context)).hexdigest()
    thumbnail_path = THUMBNAILS_DIR / f'{hash}.png'

    if not thumbnail_path.exists():
        thumbnail_bytes = render(url_for_static=url_for_static, **context)
        thumbnail_path.write_bytes(thumbnail_bytes)
    return thumbnail_path.relative_to(STATIC_DIR)


def url_for_static(filename):
    path = STATIC_DIR / filename
    return f'file://{path.resolve()}'


def render(**context):
    template_path = Path(__file__).parent / 'templates' / 'thumbnail.html'
    html = Template(template_path.read_text()).render(**context)

    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        f.write(html.encode('utf-8'))
    try:
        with tempfile.TemporaryDirectory() as dir_path:
            # pageres doesn't support changing the output directory, so we need
            # to set cwd. The problem is, with cwd set to temp dir, npx stops
            # to work, therefore we need to use an explicit path here
            pageres = ['node', f'{os.getcwd()}/node_modules/.bin/pageres']
            run(pageres + [f'file://{f.name}', '1200x630',
                '--format=png', '--overwrite', '--filename=thumbnail'],
               cwd=dir_path, check=True, stdout=DEVNULL)
            thumbnail_path = Path(dir_path) / 'thumbnail.png'
            return thumbnail_path.read_bytes()
    finally:
        os.unlink(f.name)
