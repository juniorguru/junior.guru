from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from itertools import takewhile

import click

from jg.coop.lib import loggers
from jg.coop.lib.circleci import PROJECT_ID, create_client, get_data, get_workflow_url


logger = loggers.from_path(__file__)


RUNS_MAX_AGE = timedelta(days=3)


@click.command()
@click.argument("circleci_branch", envvar="CIRCLE_BRANCH")
@click.argument("circleci_workflow_id", envvar="CIRCLE_WORKFLOW_ID")
@click.option("--production", envvar="CIRCLECI")
@click.option("--circleci-api-key", envvar="CIRCLECI_API_KEY")
def main(circleci_branch, circleci_workflow_id, production, circleci_api_key):
    with create_client(circleci_api_key) as client:
        runs = get_recent_runs(
            get_data(client, "/runs", {"filter[project_id]": PROJECT_ID}),
            datetime.now(UTC) - RUNS_MAX_AGE,
        )
        workflows = [
            workflow
            for run in runs
            if get_run_branch(run) == circleci_branch
            for workflow in get_data(
                client, "/workflows", {"filter[run_id]": run["id"]}
            )
        ]
        for workflow in get_workflows_to_cancel(workflows, circleci_workflow_id):
            url = get_workflow_url(get_run_number(workflow, runs), workflow["id"])
            if production:
                logger.info(f"Canceling {url}")
                client.post(
                    f"/workflows/{workflow['id']}/cancel", json={}
                ).raise_for_status()
            else:
                logger.info(f"Would cancel {url}")


def get_recent_runs(runs: Iterable[dict], since: datetime) -> list[dict]:
    """Takes runs (newest first) until reaching one created before given time"""
    return list(
        takewhile(
            lambda run: parse_datetime(run["attributes"]["created_at"]) >= since,
            runs,
        )
    )


def get_run_branch(run: dict) -> str | None:
    return run["references"]["event"]["attributes"].get("vcs", {}).get("branch")


def get_workflows_to_cancel(
    workflows: list[dict], current_workflow_id: str
) -> list[dict]:
    running_workflows = {
        workflow["id"]: workflow
        for workflow in workflows
        if workflow["attributes"]["phase"] != "ended"
    }
    current_workflow = running_workflows.pop(current_workflow_id)
    created_at = parse_datetime(current_workflow["attributes"]["created_at"])
    return [
        workflow
        for workflow in running_workflows.values()
        if parse_datetime(workflow["attributes"]["created_at"]) < created_at
    ]


def get_run_number(workflow: dict, runs: list[dict]) -> int:
    run_id = workflow["references"]["run"]["id"]
    return next(run["attributes"]["number"] for run in runs if run["id"] == run_id)


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)
