import json
import subprocess
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


class OnePasswordError(Exception):
    pass


@dataclass
class OnePasswordItem:
    account: str
    vault: str
    item: str


def get_password(item: OnePasswordItem) -> str | None:
    """Returns the password field of a 1Password item of type Password, if not empty"""
    logger.debug(f"Reading password of 1Password item {item.item}")
    return parse_password(run(build_command(item, "get", "--format", "json")))


def set_password(item: OnePasswordItem, value: str) -> None:
    logger.debug(f"Writing password of 1Password item {item.item}")
    # The value ends up on the command line of the op process, where other
    # users of the same machine can see it. Fine for a solo developer machine.
    run(build_command(item, "edit", f"password={value}"))


def run(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except FileNotFoundError as e:
        raise OnePasswordError(f"1Password CLI (op) not found: {e}") from e
    if result.returncode:
        raise OnePasswordError(f"op said: {result.stderr.strip()}")
    return result.stdout


def build_command(item: OnePasswordItem, subcommand: str, *args: str) -> list[str]:
    return [
        "op",
        "item",
        subcommand,
        item.item,
        *args,
        "--vault",
        item.vault,
        "--account",
        item.account,
    ]


def parse_link(link: str) -> OnePasswordItem | None:
    """Returns IDs from a private link to a 1Password item, or nothing if it's not one"""
    url = urlparse(link)
    if url.scheme != "https" or not url.netloc.endswith("1password.com"):
        return None
    params = parse_qs(url.query)
    try:
        return OnePasswordItem(
            account=params["a"][0], vault=params["v"][0], item=params["i"][0]
        )
    except KeyError as e:
        raise ValueError(
            "Expected a private link to a 1Password item, "
            f"with a=, v=, and i= in it, got {link!r}"
        ) from e


def parse_password(item_json: str) -> str | None:
    """Returns the value of the password field of a 1Password item, if any"""
    for field in json.loads(item_json).get("fields", []):
        if field.get("purpose") == "PASSWORD" or field.get("id") == "password":
            return field.get("value") or None
    return None
