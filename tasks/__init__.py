import os
import sys
from datetime import datetime, timedelta

import pytest
from invoke import Collection, Exit, task
import requests

from juniorguru.utils import checks
from juniorguru.utils.screenshots import main as screenshots
from juniorguru.utils.students import main as students
from juniorguru.utils.participant import main as participant
from juniorguru.utils.winners import main as winners

from . import sync, web


@task(incrementable=['v'])
def test(context, v=0, x=False):
    args = (v * ['-v']) + (int(x) * ['-x'])
    code = pytest.main(args)
    if code:
        raise Exit(code=code)


@task()
def lint(context):
    context.run('poetry run flake8')
    context.run("npx stylelint 'juniorguru/scss/**/*.*css' 'juniorguru/image_templates/*.*css'")


@task()
def format(context):
    context.run('poetry run isort .')


@task()
def cancel_previous_builds(context):
    if not os.getenv('CIRCLECI'):
        print('Not CircleCI', file=sys.stderr)
        raise Exit(code=1)

    branch = os.environ['CIRCLE_BRANCH']
    if not branch:
        print('Unable to get CircleCI branch', file=sys.stderr)
        raise Exit(code=1)

    response = requests.get('https://circleci.com/api/v2/project/github/honzajavorek/junior.guru/pipeline',
                            params={'branch': branch},
                            headers={'Circle-Token': os.environ['CIRCLECI_API_KEY']})
    response.raise_for_status()

    day_ago = datetime.utcnow() - timedelta(days=3)
    pipelines = [pipeline for pipeline in response.json()['items']
                 if datetime.fromisoformat(pipeline['created_at'].rstrip('Z')) > day_ago]

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
        print(f"Canceling https://app.circleci.com/pipelines/github/honzajavorek/junior.guru/{workflow['pipeline_number']}/workflows/{workflow['id']}", file=sys.stderr)
        response = requests.post(f"https://circleci.com/api/v2/workflow/{workflow['id']}/cancel",
                                    headers={'Circle-Token': os.environ['CIRCLECI_API_KEY']})
        response.raise_for_status()


namespace = Collection(test, lint, format, screenshots, winners, students, participant, cancel_previous_builds,
                       sync, web, checks)
