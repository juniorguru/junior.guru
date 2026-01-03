import hashlib
import shutil
import subprocess
import warnings
from functools import cache, wraps
from pathlib import Path
from time import perf_counter

import click
from livereload import Server
from lxml import html
from mkdocs.__main__ import build_command as _build_mkdocs

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


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
@click.option("--purge/--no-purge", default=True)
@click.pass_context
@building("everything")
def build(context, output_path: Path, purge: bool):
    shutil.rmtree(output_path, ignore_errors=True)
    output_path.mkdir(parents=True, exist_ok=True)
    context.invoke(build_mkdocs, output_path=output_path)
    context.invoke(build_static, output_path=output_path)
    if purge:
        purge_css(output_path)


def purge_css(output_path: Path):
    """Remove unused CSS rules by scanning generated HTML."""
    logger.info("Purging unused CSS")
    css_file = output_path / "static" / "css" / "index.css"
    subprocess.run(
        [
            "npx",
            "purgecss",
            "--css", str(css_file),
            "--content", str(output_path / "**/*.html"),
            "--output", str(css_file.parent),
            "--safelist", "active", "matching", "open", "noscript",
        ],
        check=True,
    )


@main.command()
@click.argument("output_path", default="public", type=click.Path(path_type=Path))
@click.option("--open/--no-open", default=False)
@click.option("--css-purge", is_flag=True, default=False)
@click.pass_context
def serve(context, output_path: Path, open: bool, css_purge: bool):
    context.invoke(build, output_path=output_path, purge=css_purge)

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
        html_tree = html.fromstring(html_path.read_text())

        # Cache busting CSS
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching#cache_busting
        for link in html_tree.cssselect('link[href$=".css"]'):
            href = link.get("href")
            try:
                css_path = resolve_path(output_path, html_path, href)
            except ValueError as e:
                logger["postprocess"].debug(str(e))
            else:
                logger["postprocess"].debug(f"Cache busting {href} ({css_path})")
                href = f"{href}?hash={hash_file(css_path)}"
                link.set("href", href)

        # Cache busting JS
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching#cache_busting
        for script in html_tree.cssselect('script[src$=".js"]'):
            src = script.get("src")
            try:
                js_path = resolve_path(output_path, html_path, src)
            except ValueError as e:
                logger["postprocess"].debug(str(e))
            else:
                logger["postprocess"].debug(f"Cache busting {src} ({js_path})")
                src = f"{src}?hash={hash_file(js_path)}"
                script.set("src", src)

        html_path.write_text(html.tostring(html_tree, encoding="unicode"))


def resolve_path(output_path: Path, html_path: Path, url: str):
    if url.startswith("http"):
        raise ValueError(f"Cannot resolve external URL: {url}")
    if url.startswith("/"):
        return (output_path / url.lstrip("/")).resolve()
    return (html_path.parent / url).resolve()


@cache
def hash_file(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()
