from io import BytesIO
import itertools
import math
import subprocess
from pathlib import Path

import click
from PIL import Image

from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


@click.group(invoke_without_command=True)
@click.pass_context
def main(context):
    if context.invoked_subcommand:
        return
    context.invoke(python_code)
    context.invoke(avatars)
    context.invoke(svg)


@main.command()
def python_code():
    try:
        subprocess.run(['isort', '.'], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
@click.option('--size', 'size_px', default=500, type=int)
def avatars(size_px):
    images_dir = Path('juniorguru/images')
    paths = itertools.chain((images_dir / 'avatars-participants').rglob('*.jpg'),
                            (images_dir / 'avatars-quotes').rglob('*.jpg'),
                            (images_dir / 'stories').rglob('*.jpg'))
    for path in paths:
        logger.debug(f'{path.relative_to(images_dir)}')
        size_before = kilobytes(path.stat().st_size)
        buffer = BytesIO()
        with Image.open(path) as image:
            if image.width != image.height:
                raise ValueError(f"Image {path} must be square, but is {image.width}x{image.height}")
            if image.width > size_px:
                image = image.resize((size_px, size_px))
            image.save(buffer, 'JPEG', optimize=True, quality=85)
        image_bytes = buffer.getvalue()
        size_after = kilobytes(len(image_bytes))
        if size_after < size_before:
            path.write_bytes(image_bytes)
            logger.info(f'{path.relative_to(images_dir)}: {size_before}kB → {size_after}kB')


@main.command()
def svg():
    paths = Path('juniorguru/images').rglob('*.svg')
    for path in paths:
        print(path)
    # TODO scour


def kilobytes(size):
    return math.ceil(size / 1000)
