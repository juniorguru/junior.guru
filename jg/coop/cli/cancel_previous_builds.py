from datetime import date, datetime, timedelta

import click
from pycircleci.api import Api

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


@click.command()
@click.argument("circleci_branch", envvar="CIRCLE_BRANCH")
@click.argument("circleci_workflow_id", envvar="CIRCLE_WORKFLOW_ID")
@click.option("--production", envvar="CIRCLECI")
@click.option("--circleci-api-key", envvar="CIRCLECI_API_KEY")
def main(circleci_branch, circleci_workflow_id, production, circleci_api_key):
    circleci = Api(token=circleci_api_key)
    pipelines = circleci.get_project_pipelines(
        "juniorguru", "junior.guru", branch=circleci_branch, paginate=True
    )
    days_ago = date.today() - timedelta(days=3)
    pipelines = [
        pipeline
        for pipeline in pipelines
        if datetime.fromisoformat(pipeline["created_at"].rstrip("Z")).date() > days_ago
    ]

    running_workflows = {}
    for pipeline in pipelines:
        workflows = circleci.get_pipeline_workflow(pipeline["id"], paginate=True)
        running_workflows.update(
            (workflow["id"], workflow)
            for workflow in workflows
            if workflow["status"] == "running"
        )

    current_workflow = running_workflows.pop(circleci_workflow_id)
    created_at = datetime.fromisoformat(current_workflow["created_at"].rstrip("Z"))
    workflows_to_cancel = [
        workflow
        for workflow in running_workflows.values()
        if datetime.fromisoformat(workflow["created_at"].rstrip("Z")) < created_at
    ]

    for workflow in workflows_to_cancel:
        url = (
            "https://app.circleci.com/pipelines/"
            "github/juniorguru/junior.guru"
            f"/{workflow['pipeline_number']}/workflows/{workflow['id']}"
        )
        if production:
            logger.info(f"Canceling {url}")
            circleci.cancel_workflow(workflow["id"])
        else:
            logger.info(f"Would cancel {url}")
