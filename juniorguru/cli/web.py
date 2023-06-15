import shutil
import subprocess
import warnings
from functools import wraps
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

import click
from livereload import Server
from mkdocs.__main__ import build_command as mkdocs_build

from juniorguru.lib import loggers
from juniorguru.web_legacy.__main__ import main as flask_freeze


logger = loggers.from_path(__file__)


@click.group()
def main():
    pass


def building(title: str):
    def decorator(command):
        @wraps(command)
        def wrapper(*args, **kwargs):
            time_start = perf_counter()
            logger.info(f'Building {title}')
            return_value = command(*args, **kwargs)
            time_end = perf_counter() - time_start
            logger.info(f'Done building {title} in {time_end:.2f}s')
            return return_value
        return wrapper
    return decorator


@main.command()
@click.argument('output_path', default='public', type=click.Path(path_type=Path))
@building('static files')
def build_static(output_path: Path):
    static_path = output_path / 'static'
    shutil.copytree('juniorguru/images', static_path, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('screenshots-overrides'))
    shutil.copytree('juniorguru/images/screenshots-overrides', static_path / 'screenshots', dirs_exist_ok=True)
    subprocess.run(['node', 'esbuild.js', str(static_path.absolute())], check=True)
    Path(static_path / 'favicon.ico').rename(output_path / 'favicon.ico')


@main.command()
@click.argument('output_path', default='public', type=click.Path(path_type=Path))
@building('Flask files')
def build_flask(output_path: Path):
    flask_freeze(output_path)


@main.command()
@click.pass_context
@click.argument('config', default='juniorguru/web/mkdocs.yml', type=click.Path(exists=True, path_type=Path))
@click.argument('output_path', default='public', type=click.Path(path_type=Path))
@click.option('-w', '--warnings/--no-warnings', 'warn', default=False)
@building('MkDocs files')
def build_mkdocs(context, config: Path, output_path: Path, warn: bool):
    _simplefilter = warnings.simplefilter
    if not warn:
        # Unfortunately MkDocs sets their own warnings filter, so we have to
        # nuke the whole thing to disable warnings. This is a hack, but it works.
        warnings.simplefilter = lambda *args, **kwargs: None

    # Unfortunately MkDocs doesn't support mixing with existing files inside
    # the output directory, so we have to build into a temporary directory and
    # then move the files over manually.
    with TemporaryDirectory() as temp_dir:
        try:
            context.invoke(mkdocs_build,
                           config_file=str(config.absolute()),
                           site_dir=temp_dir)
            shutil.copytree(temp_dir, output_path.absolute(), dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('sitemap.xml*'))
        finally:
            warnings.simplefilter = _simplefilter


@main.command()
@click.argument('output_path', default='public', type=click.Path(path_type=Path))
@click.pass_context
@building('everything')
def build(context, output_path: Path):
    shutil.rmtree(output_path, ignore_errors=True)
    output_path.mkdir(parents=True, exist_ok=True)
    context.invoke(build_static, output_path=output_path)
    context.invoke(build_flask, output_path=output_path)
    context.invoke(build_mkdocs, output_path=output_path)


@main.command()
@click.argument('output_path', default='public', type=click.Path(path_type=Path))
@click.option('--open/--no-open', default=True)
@click.pass_context
def serve(context, output_path: Path, open: bool):
    context.invoke(build, output_path=output_path)

    def ignore_data(path):
        return Path(path).suffix in ['.db-shm', '.db-wal', '.log']

    def rebuild_static():
        context.invoke(build_static, output_path=output_path)

    def rebuild_flask_and_mkdocs():
        context.invoke(build_flask, output_path=output_path)
        context.invoke(build_mkdocs, output_path=output_path)

    def rebuild_mkdocs():
        context.invoke(build_mkdocs, output_path=output_path)

    server = Server()
    server.setHeader('Access-Control-Allow-Origin', '*')
    server.watch('juniorguru/**/*.js', rebuild_static)
    server.watch('juniorguru/**/*.scss', rebuild_static)
    server.watch('juniorguru/images/', rebuild_static)
    server.watch('juniorguru/data/', rebuild_flask_and_mkdocs, ignore=ignore_data)
    server.watch('juniorguru/lib/', rebuild_flask_and_mkdocs)
    server.watch('juniorguru/models/', rebuild_flask_and_mkdocs)
    server.watch('juniorguru/web/', rebuild_mkdocs)
    server.watch('juniorguru/web_legacy/', rebuild_flask_and_mkdocs)
    server.serve(host='localhost',
                 root=str(output_path.absolute()),
                 open_url_delay=0.1 if open else None)
