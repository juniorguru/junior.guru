import itertools
import math
import subprocess
from io import BytesIO
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
    context.invoke(format_python)
    context.invoke(optimize_avatars)
    context.invoke(optimize_svg)


@main.command()
def format_python():
    try:
        subprocess.run(['isort', '.'], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
@click.option('--size', 'size_px', default=500, type=int)
def optimize_avatars(size_px):
    images_dir = Path('juniorguru/images')
    paths = itertools.chain.from_iterable(avatars_dir.rglob('*.jpg')
                                          for avatars_dir
                                          in images_dir.glob('avatars-*'))
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
def optimize_svg():
    images_dir = Path('juniorguru/images')
    paths = images_dir.rglob('*.svg')
    for path in paths:
        logger.debug(f'{path.relative_to(images_dir)}')
        size_before = kilobytes(path.stat().st_size)
        proc = subprocess.run(['scour', '-i', str(path)], check=True, capture_output=True)
        image_bytes = proc.stdout
        size_after = kilobytes(len(image_bytes))
        if size_after < size_before:
            path.write_bytes(image_bytes)
            logger.info(f'{path.relative_to(images_dir)}: {size_before}kB → {size_after}kB')


def kilobytes(size):
    return math.ceil(size / 1000)
