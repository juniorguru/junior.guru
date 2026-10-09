"""Downloads original files of dependencies the PR adds or changes, without installing them

Compares uv.lock and package-lock.json with a base git ref, downloads each new or changed
package as locked, verifies its hash, and unpacks it, so that Claude can audit it.
Nothing in this script executes code of the packages.
"""

import base64
import hashlib
import json
import shutil
import subprocess
import sys
import tarfile
import tomllib
import urllib.request
import zipfile
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Artifact:
    url: str
    hash: str  # in the 'algorithm:hexdigest' format


@dataclass(frozen=True)
class Change:
    ecosystem: str
    name: str
    version: str
    base_versions: tuple[str, ...]
    source: str
    artifacts: tuple[Artifact, ...] = ()
    git_url: str | None = None
    git_commit: str | None = None

    @property
    def dir_name(self) -> str:
        return f"{self.ecosystem}-{self.name.replace('/', '__')}-{self.version}"


def main() -> None:
    base_ref, output_dir = sys.argv[1], Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    changes = get_uv_changes(
        read_toml(git_show(base_ref, "uv.lock")), read_toml(Path("uv.lock").read_text())
    ) + get_npm_changes(
        read_json(git_show(base_ref, "package-lock.json")),
        read_json(Path("package-lock.json").read_text()),
    )
    lines = ["# Dependencies added or changed by the PR", ""]
    if not changes:
        lines.append("None.")
    for change in changes:
        print(f"Downloading {change.dir_name}", flush=True)
        try:
            download(change, output_dir / change.dir_name)
            status = f"`{change.dir_name}/`"
        except Exception as exc:
            status = f"download failed: {exc}"
        base = ", ".join(change.base_versions) or "new"
        lines.append(
            f"- {change.ecosystem} `{change.name}` {base} → {change.version} "
            f"(source: {change.source}): {status}"
        )
    (output_dir / "index.md").write_text("\n".join(lines) + "\n")


def get_uv_changes(base: dict[str, Any], head: dict[str, Any]) -> list[Change]:
    base_keys = {uv_key(package) for package in base.get("package", [])}
    changes = []
    for package in head.get("package", []):
        source = package["source"]
        if uv_key(package) in base_keys or not (
            "registry" in source or "git" in source
        ):
            continue
        base_versions = tuple(
            base_package["version"]
            for base_package in base.get("package", [])
            if base_package["name"] == package["name"]
        )
        if "git" in source:
            url, _, commit = source["git"].partition("#")
            changes.append(
                Change(
                    ecosystem="pypi",
                    name=package["name"],
                    version=package["version"],
                    base_versions=base_versions,
                    source=source["git"],
                    git_url=url.partition("?")[0],
                    git_commit=commit,
                )
            )
        else:
            artifacts = [package["sdist"]] if "sdist" in package else []
            if wheel := pick_wheel(package.get("wheels", [])):
                artifacts.append(wheel)
            changes.append(
                Change(
                    ecosystem="pypi",
                    name=package["name"],
                    version=package["version"],
                    base_versions=base_versions,
                    source=source["registry"],
                    artifacts=tuple(
                        Artifact(url=artifact["url"], hash=artifact["hash"])
                        for artifact in artifacts
                    ),
                )
            )
    return changes


def uv_key(package: dict[str, Any]) -> tuple[str, str, str]:
    return (
        package["name"],
        package["version"],
        json.dumps(package["source"], sort_keys=True),
    )


def pick_wheel(wheels: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Picks the wheel uv would install on the CI runner, or any as a fallback"""
    for suffix in ("-none-any.whl", "manylinux_2_17_x86_64.whl", "x86_64.whl"):
        for wheel in wheels:
            if wheel["url"].endswith(suffix):
                return wheel
    return wheels[0] if wheels else None


def get_npm_changes(base: dict[str, Any], head: dict[str, Any]) -> list[Change]:
    base_packages = npm_packages(base)
    changes = []
    for (name, version), package in npm_packages(head).items():
        if (name, version) in base_packages or "resolved" not in package:
            continue
        changes.append(
            Change(
                ecosystem="npm",
                name=name,
                version=version,
                base_versions=tuple(
                    base_version
                    for base_name, base_version in base_packages
                    if base_name == name
                ),
                source=package["resolved"],
                artifacts=(
                    Artifact(
                        url=package["resolved"],
                        hash=npm_integrity_to_hash(package["integrity"]),
                    ),
                ),
            )
        )
    return changes


def npm_packages(lock: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (path.rpartition("node_modules/")[2], package["version"]): package
        for path, package in lock.get("packages", {}).items()
        if path and "version" in package
    }


def npm_integrity_to_hash(integrity: str) -> str:
    algorithm, _, digest = integrity.partition("-")
    return f"{algorithm}:{base64.b64decode(digest).hex()}"


def download(change: Change, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    if change.git_url:
        git_clone(change.git_url, change.git_commit or "HEAD", target_dir)
    for artifact in change.artifacts:
        content = fetch(artifact.url)
        algorithm, _, expected = artifact.hash.partition(":")
        if (actual := hashlib.new(algorithm, content).hexdigest()) != expected:
            raise ValueError(f"hash mismatch for {artifact.url}: {actual}")
        filename = artifact.url.rpartition("/")[2]
        unpack(filename, content, target_dir / strip_archive_suffix(filename))


def git_clone(url: str, commit: str, target_dir: Path) -> None:
    for args in (
        ["init", "--quiet"],
        ["fetch", "--quiet", "--depth=1", url, commit],
        ["checkout", "--quiet", "FETCH_HEAD"],
    ):
        subprocess.run(["git", *args], cwd=target_dir, check=True)
    shutil.rmtree(target_dir / ".git")


def strip_archive_suffix(filename: str) -> str:
    for suffix in (".tar.gz", ".tgz", ".whl", ".zip"):
        if filename.endswith(suffix):
            return filename.removesuffix(suffix)
    return filename


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def unpack(filename: str, content: bytes, target_dir: Path) -> None:
    if filename.endswith((".whl", ".zip")):
        with zipfile.ZipFile(BytesIO(content)) as archive:
            archive.extractall(target_dir)
    else:
        with tarfile.open(fileobj=BytesIO(content)) as archive:
            archive.extractall(target_dir, filter="data")


def git_show(ref: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"], capture_output=True, text=True, check=False
    )
    return result.stdout if result.returncode == 0 else None


def read_toml(text: str | None) -> dict[str, Any]:
    return tomllib.loads(text) if text else {}


def read_json(text: str | None) -> dict[str, Any]:
    return json.loads(text) if text else {}


if __name__ == "__main__":
    main()
