from datetime import datetime

import click
import httpx2

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


API_URL = "https://circleci.com/api/v3"

PROJECT_ID = "ecf683af-646e-4014-8483-a95ab98fa816"  # gh/juniorguru/junior.guru

RUNS_LIMIT = 20


@click.command()
@click.argument("circleci_branch", envvar="CIRCLE_BRANCH")
@click.argument("circleci_workflow_id", envvar="CIRCLE_WORKFLOW_ID")
@click.option("--production", envvar="CIRCLECI")
@click.option("--circleci-api-key", envvar="CIRCLECI_API_KEY")
def main(circleci_branch, circleci_workflow_id, production, circleci_api_key):
    headers = (
        {"Authorization": f"Bearer {circleci_api_key}"} if circleci_api_key else {}
    )
    with httpx2.Client(base_url=API_URL, headers=headers, timeout=30) as client:
        runs = get_data(
            client,
            "/runs",
            {"filter[project_id]": PROJECT_ID, "page[limit]": RUNS_LIMIT},
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
            url = get_workflow_url(workflow, runs)
            if production:
                logger.info(f"Canceling {url}")
                client.post(
                    f"/workflows/{workflow['id']}/cancel", json={}
                ).raise_for_status()
            else:
                logger.info(f"Would cancel {url}")


def get_data(client: httpx2.Client, path: str, params: dict) -> list[dict]:
    response = client.get(path, params=params)
    response.raise_for_status()
    return response.json()["data"]


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


def get_workflow_url(workflow: dict, runs: list[dict]) -> str:
    run_id = workflow["references"]["run"]["id"]
    run_number = next(
        run["attributes"]["number"] for run in runs if run["id"] == run_id
    )
    return (
        "https://app.circleci.com/pipelines/github/juniorguru/junior.guru"
        f"/{run_number}/workflows/{workflow['id']}"
    )


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.rstrip("Z"))
