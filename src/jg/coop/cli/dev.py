import re
import shutil
import subprocess
import sys
from pathlib import Path

import click
import pytest
from ghp_import import ghp_import

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


@click.group()
def main():
    pass


@main.command()
@click.option("--pull/--no-pull", default=True)
@click.option("--packages/--no-packages", default=True)
@click.option("--push/--no-push", default=True)
@click.option("--stash/--no-stash", default=False)
def update(pull, packages, push, stash):
    try:
        logger.info("Terminating running processes")
        python_path = sys.executable
        jg_path = f"{python_path.removesuffix('/python')}/jg"
        subprocess.run(["pgrep", "-fl", jg_path])  # prints what's getting terminated
        subprocess.run(["pkill", "-SIGTERM", "-f", jg_path])
        if stash:
            logger.info("Stashing work in progress")
            subprocess.run(["git", "stash"], check=True)
        if pull:
            logger.info("Pulling changes")
            subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
        if packages:
            logger.info("Upgrading packages")
            uv_upgrade()
            subprocess.run(["npm", "update"], check=True)
            subprocess.run(["npm", "install"], check=True)
            subprocess.run(
                ["git", "add", "pyproject.toml", "uv.lock", "package-lock.json"]
            )
            subprocess.run(["git", "commit", "-m", "update packages 📦"])
        else:
            logger.info("Installing packages")
            subprocess.run(["uv", "install"], check=True)
            subprocess.run(["npm", "install"], check=True)
        logger.info("Installing Playwright browsers")
        subprocess.run(["playwright", "install", "firefox"], check=True)
        if push:
            logger.info("Pushing changes")
            subprocess.run(["git", "push"], check=True)
        if stash:
            logger.info("Getting work in progress back from stash")
            subprocess.run(["git", "stash", "pop"], check=True)
        logger.info("Removing the 'public' directory")
        shutil.rmtree("public", ignore_errors=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


def uv_upgrade():
    changes = []
    while True:
        logger.debug("Upgrading Python packages")
        result = subprocess.run(
            ["uv", "sync", "--upgrade"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            break
        # TODO
        # if "version solving failed" in result.stderr:
        #     logger.warning("Version solving failed")
        #     if match := re.search(
        #         r"(requires|which depends on) (?P<package>\S+) \((?P<version>[^\)]+)\)",
        #         result.stderr,
        #     ):
        #         package, version = match.group("package"), match.group("version")
        #         changes.append(f"{package}=={version}")
        #         subprocess.run(["poetry", "remove", package], check=True)
        #         continue
        logger.error(f"Failed to update Python packages:\n{result.stderr}")
        raise click.Abort()
    if changes:
        logger.warning(f"Changes: {', '.join(changes)}")
        subprocess.run(["uv", "add"] + changes, check=True)


@main.command()
@click.option("-v", "--verbose", is_flag=True)
def test(verbose: bool):
    logger.info("Running Python tests")
    code = pytest.main(["-v"] if verbose else [])
    if code:
        raise click.Abort()

    logger.info("Running JavaScript tests")
    try:
        subprocess.run(
            ["npx", "vitest", "--dir=tests", "--run", "--environment=jsdom"], check=True
        )
    except subprocess.CalledProcessError:
        raise click.Abort()

    logger.info("Linting SCSS")
    try:
        subprocess.run(
            [
                "npx",
                "stylelint",
                "src/jg/coop/css/**/*.*css",
                "src/jg/coop/image_templates/*.*css",
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
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
