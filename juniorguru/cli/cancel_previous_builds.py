import os
from datetime import datetime, timedelta

import requests
import click


@click.command()
def main():
    if not os.getenv('CIRCLECI'):
        click.echo('Not CircleCI', err=True)
        raise click.Abort()

    branch = os.environ['CIRCLE_BRANCH']
    if not branch:
        click.echo('Unable to get CircleCI branch', err=True)
        raise click.Abort()

    response = requests.get('https://circleci.com/api/v2/project/github/honzajavorek/junior.guru/pipeline',
                            params={'branch': branch},
                            headers={'Circle-Token': os.environ['CIRCLECI_API_KEY']})
    response.raise_for_status()

    recently = datetime.utcnow() - timedelta(days=3)
    pipelines = [pipeline for pipeline in response.json()['items']
                 if datetime.fromisoformat(pipeline['created_at'].rstrip('Z')) > recently]

    running_workflows = {}
    for pipeline in pipelines:
        response = requests.get(f"https://circleci.com/api/v2/pipeline/{pipeline['id']}/workflow",
                                headers={'Circle-Token': os.environ['CIRCLECI_API_KEY']})
        response.raise_for_status()
        running_workflows.update((workflow['id'], workflow) for workflow in response.json()['items']
                                 if workflow['status'] == 'running')

    current_workflow = running_workflows.pop(os.environ['CIRCLE_WORKFLOW_ID'])
    created_at = datetime.fromisoformat(current_workflow['created_at'].rstrip('Z'))
    workflows_to_cancel = [workflow for workflow in running_workflows.values() if
                           datetime.fromisoformat(workflow['created_at'].rstrip('Z')) < created_at]

    for workflow in workflows_to_cancel:
        click.echo(f"Canceling https://app.circleci.com/pipelines/github/honzajavorek/junior.guru/{workflow['pipeline_number']}/workflows/{workflow['id']}", err=True)
        response = requests.post(f"https://circleci.com/api/v2/workflow/{workflow['id']}/cancel",
                                 headers={'Circle-Token': os.environ['CIRCLECI_API_KEY']})
        response.raise_for_status()
