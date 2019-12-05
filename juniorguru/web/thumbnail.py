import os
import io
import tempfile
import pickle
from hashlib import sha256
from pathlib import Path
from subprocess import run, DEVNULL

from jinja2 import Template


def render(**context):
    path = Path(__file__).parent / 'templates' / 'thumbnail.html'
    template = Template(path.read_text())
    html = template.render(**context)

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


def thumbnail(**context):
    static_dir = Path(__file__).parent / 'static'
    images_dir = static_dir / 'images' / 'thumbnails'
    images_dir.mkdir(exist_ok=True, parents=True)

    hash = sha256(pickle.dumps(context)).hexdigest()
    thumbnail_path = images_dir / f'{hash}.png'
    if not thumbnail_path.exists():
        thumbnail_path.write_bytes(render(**context))
    return thumbnail_path.relative_to(static_dir)
