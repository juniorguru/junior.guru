import itertools
import math
import re
import subprocess
from glob import glob
from io import BytesIO
from pathlib import Path
from typing import Iterable

import click
from PIL import Image

from jg.coop.lib import loggers


JINJA_IMPORT_RE = re.compile(
    r"""
        {%\s*
            from\s+
            (?P<source>'[^']+'|"[^"]+")\s+
            import
            (?P<names>[\w\s_,]+)
        \s*%}
    """,
    re.VERBOSE,
)

JINJA_CALL_RE = re.compile(
    r"""
        {{
            -?\s*
            ([\w_]+)
            \(
        |
        {%
            -?\s*
            call\s*
            ([\w_]+)
            \(
    """,
    re.VERBOSE,
)


logger = loggers.from_path(__file__)


@click.group(invoke_without_command=True)
@click.pass_context
def main(context):
    if context.invoked_subcommand:
        return
    context.invoke(format_python)
    context.invoke(format_jinja)
    context.invoke(format_web)
    context.invoke(fix_scss)
    context.invoke(optimize_avatars)
    context.invoke(optimize_svg)


@main.command()
def format_python():
    try:
        logger.info("Fixing Python code")
        subprocess.run(["ruff", "check", "--fix"], check=True)
        logger.info("Formatting Python code")
        subprocess.run(["ruff", "format"], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
def format_web():
    try:
        logger.info("Formatting web platform code")
        subprocess.run(["npx", "@biomejs/biome", "format", "--write"], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
def fix_scss():
    try:
        logger.info("Fixing SCSS code")
        subprocess.run(
            [
                "npx",
                "stylelint",
                "src/jg/coop/css/**/*.*css",
                "src/jg/coop/image_templates/*.*css",
                "--fix",
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
def format_jinja():
    logger.info("Removing unused Jinja imports")
    cwd = Path.cwd()
    web_dir = Path("src/jg/coop/web/").resolve()
    paths = itertools.chain(
        web_dir.rglob("*.jinja"), web_dir.rglob("*.md"), web_dir.rglob("*.html")
    )
    for path in paths:
        logger.debug(path.relative_to(cwd))
        markup = path.read_text()
        imports = get_jinja_imports(markup)
        calls = get_jinja_calls(markup)
        unused_imports = imports - calls
        if unused_imports:
            logger.warning(f"Unused imports: {', '.join(unused_imports)}")
            path.write_text(replace_jinja_imports(markup, calls))


@main.command()
@click.option("--size", "size_px", default=1000, type=int)
@click.option("--glob", "glob_pattern", default="src/jg/coop/images/avatars-*/*.jpg")
def optimize_avatars(size_px: int, glob_pattern: str):
    logger.info("Optimizing avatars")
    for path in map(Path, glob(glob_pattern)):
        logger.debug(f"{path}")
        size_before = kilobytes(path.stat().st_size)
        buffer = BytesIO()
        with Image.open(path) as image:
            if image.width != image.height:
                raise ValueError(
                    f"Image {path} must be square, but is {image.width}x{image.height}"
                )
            if image.width > size_px:
                image = image.resize((size_px, size_px))
            image.save(buffer, "JPEG", optimize=True, quality=85)
        image_bytes = buffer.getvalue()
        size_after = kilobytes(len(image_bytes))
        if size_after < size_before:
            path.write_bytes(image_bytes)
            logger.info(f"{path}: {size_before}kB → {size_after}kB")
    try:
        subprocess.run(["npx", "@343dev/optimizt", glob_pattern], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
def optimize_svg():
    logger.info("Optimizing SVGs")
    images_dir = Path("src/jg/coop/images")
    paths = images_dir.rglob("*.svg")
    for path in paths:
        logger.debug(f"{path.relative_to(images_dir)}")
        size_before = kilobytes(path.stat().st_size)
        proc = subprocess.run(
            ["scour", "-i", str(path)], check=True, capture_output=True
        )
        image_bytes = proc.stdout
        size_after = kilobytes(len(image_bytes))
        if size_after < size_before:
            path.write_bytes(image_bytes)
            logger.info(
                f"{path.relative_to(images_dir)}: {size_before}kB → {size_after}kB"
            )


def kilobytes(size) -> int:
    return math.ceil(size / 1000)


def get_jinja_imports(markup: str) -> set[str]:
    all_names = set()
    matches = list(JINJA_IMPORT_RE.finditer(markup))
    if matches:
        if len(matches) > 1:
            raise ValueError("Multiple Jinja imports found")
        names = (
            name.strip()
            for name in (
                re.sub(r"\s+", " ", matches[0].group("names"))
                .strip()
                .removesuffix("with context")
                .removesuffix("without context")
                .split(",")
            )
        )
        all_names.update(names)
    return all_names


def get_jinja_calls(markup: str) -> set[str]:
    all_names = set()
    for match in JINJA_CALL_RE.finditer(markup):
        names = filter(None, match.groups())
        all_names.update(names)
    return all_names


def replace_jinja_imports(markup: str, names: Iterable[str]) -> str:
    matches = list(JINJA_IMPORT_RE.finditer(markup))
    if matches:
        if len(matches) > 1:
            raise ValueError("Multiple Jinja imports found")
        match = matches[0]
        old_names = match.group("names").strip()
        new_names = ", ".join(sorted(names))
        if old_names.endswith("with context"):
            new_names += " with context"
        if old_names.endswith("without context"):
            new_names += " without context"
        new_import = f"{{% from {match.group('source')} import {new_names} %}}"
        return JINJA_IMPORT_RE.sub(new_import, markup)
    return markup
