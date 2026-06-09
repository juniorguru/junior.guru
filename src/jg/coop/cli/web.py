import hashlib
import re
import shutil
import subprocess
import warnings
from functools import cache, wraps
from pathlib import Path
from time import perf_counter

import click
from bs4 import BeautifulSoup
from livereload import Server
from mkdocs.__main__ import build_command as _build_mkdocs
from PIL import Image

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)

CSS_LINK_RE = re.compile(
    r"""
    (
        <link\b
        [^>]*              # any attributes before href
        \bhref\s*=\s*["']  # href= with opening quote
    )
    ([^"']+\.css)          # CSS URL value (without surrounding quotes)
    (["'])                 # closing quote
    """,
    re.IGNORECASE | re.VERBOSE,
)

JS_SCRIPT_RE = re.compile(
    r"""
    (
        <script\b
        [^>]*              # any attributes before src
        \bsrc\s*=\s*["']   # src= with opening quote
    )
    ([^"']+\.js)           # JS URL value (without surrounding quotes)
    (["'])                 # closing quote
    """,
    re.IGNORECASE | re.VERBOSE,
)

IMG_TAG_RE = re.compile(r"""<img\b[^>]*>""", re.IGNORECASE)


@click.group()
def main():
    pass


def building(title: str):
    def decorator(command):
        @wraps(command)
        def wrapper(*args, **kwargs):
            time_start = perf_counter()
            logger.info(f"Building {title}")
            return_value = command(*args, **kwargs)
            time_end = perf_counter() - time_start
            logger.info(f"Done building {title} in {time_end:.2f}s")
            return return_value

        return wrapper

    return decorator


@main.command()
@click.argument("output_path", default="public", type=click.Path(path_type=Path))
@building("static files")
def build_static(output_path: Path):
    static_path = output_path / "static"
    shutil.copytree(
        "src/jg/coop/images",
        static_path,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("screenshots-overrides"),
    )
    shutil.copytree(
        "src/jg/coop/images/screenshots-overrides",
        static_path / "screenshots",
        dirs_exist_ok=True,
    )
    subprocess.run(["node", "esbuild.js", str(static_path.absolute())], check=True)
    Path(static_path / "favicon.ico").rename(output_path / "favicon.ico")


@main.command()
@click.pass_context
@click.argument("output_path", default="public", type=click.Path(path_type=Path))
@click.argument(
    "config_path",
    default="src/jg/coop/web/mkdocs.yml",
    type=click.Path(exists=True, path_type=Path),
)
@click.option("-w", "--warnings/--no-warnings", "warn", default=False)
@building("MkDocs files")
def build_mkdocs(context, config_path: Path, output_path: Path, warn: bool):
    _simplefilter = warnings.simplefilter
    if not warn:
        # Unfortunately MkDocs sets their own warnings filter, so we have to
        # nuke the whole thing to disable warnings. This is a hack, but it works.
        warnings.simplefilter = lambda *args, **kwargs: None
    hidden_static_path = output_path / ".static"
    static_path = output_path / "static"
    try:
        # Trick MkDocs into ignoring static files
        static_path.rename(hidden_static_path)
    except FileNotFoundError:
        pass
    try:
        context.invoke(
            _build_mkdocs,
            config_file=str(config_path.absolute()),
            site_dir=str(output_path.absolute()),
            theme=None,
        )
    finally:
        try:
            hidden_static_path.rename(static_path)
        except FileNotFoundError:
            pass
        warnings.simplefilter = _simplefilter


@main.command()
@click.argument("output_path", default="public", type=click.Path(path_type=Path))
@click.pass_context
@building("everything")
def build(context, output_path: Path):
    shutil.rmtree(output_path, ignore_errors=True)
    output_path.mkdir(parents=True, exist_ok=True)
    context.invoke(build_mkdocs, output_path=output_path)
    context.invoke(build_static, output_path=output_path)


@main.command()
@click.argument("output_path", default="public", type=click.Path(path_type=Path))
@click.option("--open/--no-open", default=False)
@click.pass_context
def serve(context, output_path: Path, open: bool):
    context.invoke(build, output_path=output_path)

    def ignore_data(path) -> bool:
        return Path(path).suffix in [".db-shm", ".db-wal", ".log"]

    def rebuild_static():
        context.invoke(build_static, output_path=output_path)

    def rebuild_mkdocs():
        subprocess.run(["jg", "web", "build-mkdocs", str(output_path)], check=True)

    server = Server()
    server.setHeader("Access-Control-Allow-Origin", "*")
    server.watch("src/jg/coop/**/*.js", rebuild_static)
    server.watch("src/jg/coop/**/*.scss", rebuild_static)
    server.watch("src/jg/coop/images/", rebuild_static)
    server.watch("src/jg/coop/data/", rebuild_mkdocs, ignore=ignore_data)
    server.watch("src/jg/coop/lib/", rebuild_mkdocs)
    server.watch("src/jg/coop/models/", rebuild_mkdocs)
    server.watch("src/jg/coop/web/", rebuild_mkdocs)
    server.serve(
        host="localhost",
        root=str(output_path.absolute()),
        open_url_delay=0.1 if open else None,
    )


@main.command()
@click.argument(
    "output_path", default="public", type=click.Path(exists=True, path_type=Path)
)
def post_process(output_path: Path):
    for html_path in output_path.glob("**/*.html"):
        logger["postprocess"].info(f"Post-processing {html_path}")
        html_text = html_path.read_text()
        html_text = _fill_image_dimensions(html_text, output_path, html_path)
        html_text = _cache_bust_urls(html_text, output_path, html_path)
        html_path.write_text(html_text)


def _fill_image_dimensions(html_text: str, output_path: Path, html_path: Path) -> str:
    log = logger["postprocess"]["image-dimensions"]

    def replace_img(match: re.Match[str]) -> str:
        img_tag = match.group(0)
        img = BeautifulSoup(img_tag, "html.parser").find("img")

        if img.get("width") and img.get("height"):
            log.debug(f"{img['src']}: Already has dimensions, skipping")
            return img_tag
        try:
            image_path = resolve_path(output_path, html_path, img["src"])
        except ValueError:
            log.debug(f"{img['src']}: Unable to resolve path, skipping")
            return img_tag

        if image_path.suffix.lower() == ".svg":
            log.debug(f"{image_path}: SVG, skipping")
            return img_tag

        with Image.open(image_path) as image:
            width, height = image.size

        log.info(f"{image_path}: {width}x{height}")
        img["width"], img["height"] = str(width), str(height)
        return str(img).replace("/>", ">")

    return IMG_TAG_RE.sub(replace_img, html_text)


def _cache_bust_urls(html_text: str, output_path: Path, html_path: Path) -> str:
    log = logger["postprocess"]["cache-busting"]

    def bust_url(url: str) -> str:
        try:
            file_path = resolve_path(output_path, html_path, url)
        except ValueError as e:
            log.debug(str(e))
            return url

        log.debug(f"Cache busting {url} ({file_path})")
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}hash={hash_file(file_path)}"

    def replace_url(match: re.Match[str]) -> str:
        return f"{match.group(1)}{bust_url(match.group(2))}{match.group(3)}"

    # Cache busting CSS and JS by rewriting matching URLs in-place.
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching#cache_busting
    html_text = CSS_LINK_RE.sub(replace_url, html_text)
    return JS_SCRIPT_RE.sub(replace_url, html_text)


def resolve_path(output_path: Path, html_path: Path, url: str):
    clean_url = url.split("#", 1)[0].split("?", 1)[0]
    if clean_url.startswith("http"):
        raise ValueError(f"Cannot resolve external URL: {url}")
    if clean_url.startswith("/"):
        return (output_path / clean_url.lstrip("/")).resolve()
    return (html_path.parent / clean_url).resolve()


@cache
def hash_file(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()
