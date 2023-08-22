import shutil
import subprocess
from pathlib import Path

import click
import pytest
from ghp_import import ghp_import

from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


@click.group()
def main():
    pass


@main.command()
@click.option("--pull/--no-pull", default=True)
@click.option("--push/--no-push", default=True)
@click.option("--stash/--no-stash", default=False)
def update(pull, push, stash):
    try:
        if stash:
            logger.info("Stashing work in progress")
            subprocess.run(["git", "stash"], check=True)
        if pull:
            logger.info("Pulling changes")
            subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
        if push:
            logger.info("Pushing changes")
            subprocess.run(["git", "push"], check=True)
        if stash:
            logger.info("Getting work in progress back from stash")
            subprocess.run(["git", "stash", "pop"], check=True)
        logger.info("Installing Python packages")
        subprocess.run(["poetry", "install"], check=True)
        logger.info("Updating juniorguru-chick")
        subprocess.run(["poetry", "update", "juniorguru-chick"], check=True)
        logger.info("Installing Playwright browsers")
        subprocess.run(["playwright", "install", "firefox"], check=True)
        logger.info("Installing Node packages")
        subprocess.run(["npm", "install"], check=True)
        logger.info("Removing the 'public' directory")
        shutil.rmtree("public", ignore_errors=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
def lint():
    try:
        subprocess.run(["flake8"], check=True)
        subprocess.run(
            [
                "npx",
                "stylelint",
                "juniorguru/scss/**/*.*css",
                "juniorguru/image_templates/*.*css",
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command(context_settings={"ignore_unknown_options": True})
@click.argument("pytest_args", nargs=-1, type=click.UNPROCESSED)
def test(pytest_args):
    code = pytest.main(list(pytest_args))
    if code:
        raise click.Abort()


@main.command()
@click.argument(
    "public_dir", default="public", type=click.Path(exists=True, path_type=Path)
)
@click.argument("commit_hash", envvar="CIRCLE_SHA1")
@click.argument("build_url", envvar="CIRCLE_BUILD_URL")
def deploy(public_dir: Path, commit_hash: str, build_url: str):
    message = f"deploy {commit_hash} 🐣 [skip ci]\n\n{build_url}"
    ghp_import(
        str(public_dir),
        mesg=message,
        push=True,
        force=True,
        cname="junior.guru",
        nojekyll=True,
    )


@main.command()
def reset_repo():
    try:
        subprocess.run(["git", "reset", "--hard"], check=True)
        subprocess.run(["git", "clean", "-f", "-d"], check=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option("--message", default="save changes 🛠️")
@click.option("--build-url", envvar="CIRCLE_BUILD_URL")
@click.option("--skip-ci/--no-skip-ci", default=True)
def save_changes(paths, message, build_url, skip_ci):
    if skip_ci:
        message += " [skip ci]"
    if build_url:
        message += f"\n\n{build_url}"
    try:
        for path in paths:
            logger["save-changes"].info(f"Adding path: {path}")
            subprocess.run(["git", "add", "-A", str(path)], check=True)

        proc = subprocess.run(
            ["git", "diff", "--name-only", "--cached"], stdout=subprocess.PIPE
        )
        if proc.stdout:
            logger["save-changes"].info(f"Commit message: {message!r}")
            subprocess.run(["git", "commit", "-m", message], check=True)
            logger["save-changes"].info("Pushing changes")
            subprocess.run(["git", "push"], check=True)
        else:
            logger["save-changes"].warning("No changes to push")
    except subprocess.CalledProcessError:
        raise click.Abort()


@main.command()
@click.argument(
    "path",
    default="juniorguru/data/data.db",
    type=click.Path(exists=True, path_type=Path),
)
@click.pass_context
def db(context: click.Context, path: Path):
    subprocess.run(
        ["datasette", str(path.absolute()), "--reload", "--open"], check=True
    )
