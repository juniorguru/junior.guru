import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import click

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


HISTORY_SIZE = 3

FAILURE_MAPS = ["error_map", "timeout_map"]


@click.command()
@click.argument("report_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--history-path",
    default=".lychee-history.json",
    type=click.Path(path_type=Path),
)
@click.option("--history-size", default=HISTORY_SIZE, type=int)
def main(report_path: Path, history_path: Path, history_size: int):
    """
    Fails only on links which failed in each of the last few link checks.

    Expects a JSON report from lychee (--format json). Failures from the
    current report are added to a history file, which CI caches between runs.
    """
    report = json.loads(report_path.read_text())
    failures = parse_failures(report)
    logger.info(f"Lychee reports {len(failures)} failing links")
    for url, failure in sorted(failures.items()):
        logger.info(f"Failing: {url} ({failure['status']})")

    history = load_history(history_path)
    logger.info(f"Loaded {len(history)} previous link checks from {history_path}")
    history = update_history(history, failures, datetime.now(UTC), history_size)
    history_path.write_text(json.dumps(history, indent=2, ensure_ascii=False))
    logger.info(f"Saved {len(history)} link checks to {history_path}")

    if len(history) < history_size:
        logger.warning(
            f"Only {len(history)} link checks in history, need {history_size} to detect persistently failing links"
        )
        return

    if persistent_urls := get_persistent_failures(history, history_size):
        logger.error(
            f"Links failing in each of the last {history_size} link checks: {len(persistent_urls)}"
        )
        for url in persistent_urls:
            failure = failures[url]
            sources = ", ".join(failure["sources"])
            logger.error(f"{url} ({failure['status']}) in {sources}")
        raise click.Abort()
    logger.info(f"No links failing in each of the last {history_size} link checks")


def parse_failures(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    sources = defaultdict(set)
    statuses = {}
    for map_name in FAILURE_MAPS:
        for source, responses in report.get(map_name, {}).items():
            for response in responses:
                sources[response["url"]].add(source)
                statuses[response["url"]] = format_status(response["status"])
    return {
        url: {"status": statuses[url], "sources": sorted(sources[url])}
        for url in statuses
    }


def format_status(status: dict[str, Any]) -> str:
    if details := status.get("details"):
        return f"{status['text']}: {details}"
    return status["text"]


def load_history(path: Path) -> list[dict[str, Any]]:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return []


def update_history(
    history: list[dict[str, Any]],
    failures: dict[str, dict[str, Any]],
    checked_at: datetime,
    size: int,
) -> list[dict[str, Any]]:
    entry = {"checked_at": checked_at.isoformat(), "urls": sorted(failures)}
    return [*history, entry][-size:]


def get_persistent_failures(history: list[dict[str, Any]], size: int) -> list[str]:
    if len(history) < size:
        return []
    url_sets = [set(entry["urls"]) for entry in history[-size:]]
    return sorted(set.intersection(*url_sets))
