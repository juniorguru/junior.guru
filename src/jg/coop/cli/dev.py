import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import click
import httpx2
import pytest
import yaml
from ghp_import import ghp_import

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


def run(
    args: list[str], *, check: bool = True, **kwargs
) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=check, **kwargs)


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
        jg_path = f"{python_path.removesuffix('3').removesuffix('/python')}/jg"
        run(["pgrep", "-fl", jg_path], check=False)  # prints what's getting terminated
        run(["pkill", "-SIGTERM", "-f", jg_path], check=False)
        if stash:
            logger.info("Stashing work in progress")
            run(["git", "stash"])
        if pull:
            logger.info("Pulling changes")
            run(["git", "pull", "--rebase", "origin", "main"])
        if packages:
            logger.info("Upgrading packages")
            ci_config_path = ".circleci/config.yml"
            upgrade_lychee(ci_config_path)
            run(["uv", "sync", "--upgrade"])
            run(["npm", "update"])
            run(["npm", "install"])
            paths = ["pyproject.toml", "uv.lock", "package-lock.json", ci_config_path]
            run(["git", "add"] + paths, check=False)
            run(["git", "commit", "-m", "update packages 📦"], check=False)
        else:
            logger.info("Installing packages")
            run(["uv", "install"])
            run(["npm", "install"])
        logger.info("Installing Playwright browsers")
        run(["playwright", "install", "firefox"])
        if push:
            logger.info("Pushing changes")
            run(["git", "push"])
        if stash:
            logger.info("Getting work in progress back from stash")
            run(["git", "stash", "pop"])
        logger.info("Removing the 'public' directory")
        shutil.rmtree("public", ignore_errors=True)
    except subprocess.CalledProcessError:
        raise click.Abort()


def upgrade_lychee(ci_config_path: Path | str):
    ci_config_path = Path(ci_config_path)
    config_text = ci_config_path.read_text()
    config = yaml.safe_load(config_text)

    logger.debug(f"Loaded CI config from {ci_config_path}")
    original_command = next(
        step["run"]["command"]
        for step in config["jobs"]["check-links"]["steps"]
        if "run" in step and step["run"]["name"].lower() == "download lychee"
    )
    logger.debug(f"Lychee download command: {original_command!r}")

    api_url = "https://api.github.com/repos/lycheeverse/lychee/releases/latest"
    response = httpx2.get(api_url)
    response.raise_for_status()
    linux_musl = next(
        asset
        for asset in response.json().get("assets", [])
        if "x86_64-unknown-linux-musl" in asset["name"]
    )
    download_url = linux_musl["browser_download_url"]
    logger.debug(f"Latest lychee release download URL: {download_url}")

    command_tokens = [
        (download_url if token.startswith("https://github.com/") else token)
        for token in shlex.split(original_command)
    ]
    updated_command = shlex.join(command_tokens)
    logger.debug(f"Updated lychee download command: {updated_command!r}")

    ci_config_path.write_text(config_text.replace(original_command, updated_command))
    logger.debug(f"Updated CI config written to {ci_config_path}")


@main.command()
@click.option("-v", "--verbose", is_flag=True)
def test(verbose: bool):
    logger.info("Running Python tests")
    code = pytest.main(["-v"] if verbose else [])
    if code:
        raise click.Abort()

    logger.info("Running JavaScript tests")
    try:
        run(["npx", "vitest", "--dir=tests", "--run", "--environment=jsdom"])
    except subprocess.CalledProcessError:
        raise click.Abort()

    logger.info("Linting SCSS")
    try:
        run(
            [
                "npx",
                "stylelint",
                "src/jg/coop/css/**/*.*css",
                "src/jg/coop/image_templates/*.*css",
            ]
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
        run(["git", "reset", "--hard"])
        run(["git", "clean", "-f", "-d"])
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
            run(["git", "add", "-A", str(path)])

        proc = run(
            ["git", "diff", "--name-only", "--cached"],
            stdout=subprocess.PIPE,
            check=False,
        )
        if proc.stdout:
            logger["save-changes"].info(f"Commit message: {message!r}")
            run(["git", "commit", "-m", message])
            logger["save-changes"].info("Pushing changes")
            run(["git", "push"])
        else:
            logger["save-changes"].warning("No changes to push")
    except subprocess.CalledProcessError:
        raise click.Abort()
