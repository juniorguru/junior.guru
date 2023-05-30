from pathlib import Path
from shutil import copytree, ignore_patterns
import subprocess
import warnings

import click
from mkdocs.__main__ import build_command as mkdocs_build
from juniorguru.web_legacy.__main__ import main as freeze_main


@click.group()
def main():
    pass


@main.command()
def build_static():
    copytree('juniorguru/images', 'public/static',
             dirs_exist_ok=True)
    copytree('juniorguru/images_legacy', 'public/static',
             ignore=ignore_patterns('screenshots-overrides'),
             dirs_exist_ok=True)
    subprocess.run(['node', 'esbuild.js'], check=True)
    Path('public/static/favicon.ico').rename('public/favicon.ico')


@main.command()
def build_flask():
    freeze_main('public')


@main.command()
@click.pass_context
@click.argument('config_file', default='juniorguru/web/mkdocs.yml', type=click.Path(exists=True, path_type=Path))
@click.argument('site_dir', default='public', type=click.Path(path_type=Path))
@click.option('-w', '--warnings/--no-warnings', 'warn', default=False)
def build_mkdocs(context, config_file: Path, site_dir: Path, warn: bool):
    _simplefilter = warnings.simplefilter
    if not warn:
        # Unfortunately MkDocs sets their own warnings filter, so we have to
        # nuke the whole thing to disable warnings. This is a hack, but it works.
        warnings.simplefilter = lambda *args, **kwargs: None
    try:
        context.invoke(mkdocs_build,
                       clean=False,
                       config_file=str(config_file.resolve()),
                       site_dir=str(site_dir.resolve()))
        Path('public/sitemap.xml').unlink(missing_ok=True)
        Path('public/sitemap.xml.gz').unlink(missing_ok=True)
    finally:
        warnings.simplefilter = _simplefilter


@main.command()
def build():
    raise NotImplementedError()
    subprocess.run(['npx', 'gulp', 'build'], check=True)


@main.command()
def serve():
    raise NotImplementedError()
    subprocess.run(['npx', 'gulp', 'serve'], check=True)
