"""Finds the CircleCI nightly and tells the GitHub workflow whether Claude should investigate it"""

import json
import os
import sys
import urllib.request
from datetime import UTC, datetime


API_URL = "https://circleci.com/api/v2"
PROJECT_URL_PATH = "gh/juniorguru/junior.guru"

# The job which triggers this check, it is still running while the check runs
REPORT_JOB = "report-nightly"

UNFINISHED_STATUSES = ("running", "queued", "not_running", "blocked", "on_hold")


def get(path: str) -> dict:
    with urllib.request.urlopen(f"{API_URL}{path}", timeout=30) as response:
        return json.load(response)


def find_nightly(date: str) -> dict:
    pipelines = get(f"/project/{PROJECT_URL_PATH}/pipeline?branch=main")["items"]
    for pipeline in pipelines:
        if pipeline["trigger"]["type"] != "schedule":
            continue
        for workflow in get(f"/pipeline/{pipeline['id']}/workflow")["items"]:
            if workflow["name"] == "nightly" and workflow["created_at"].startswith(
                date
            ):
                return workflow
    sys.exit(f"No nightly found for {date}")


def output(**values: str) -> None:
    with open(os.environ.get("GITHUB_OUTPUT", "/dev/stdout"), "a") as file:
        file.writelines(f"{key}={value}\n" for key, value in values.items())


def main() -> None:
    if workflow_id := os.environ.get("CIRCLECI_WORKFLOW_ID"):
        workflow = get(f"/workflow/{workflow_id}")
    else:
        workflow = find_nightly(datetime.now(UTC).date().isoformat())
    date = workflow["created_at"][:10]

    jobs = [
        job
        for job in get(f"/workflow/{workflow['id']}/job")["items"]
        if job["name"] != REPORT_JOB
    ]
    if any(job["status"] in UNFINISHED_STATUSES for job in jobs):
        sys.exit(f"Nightly for {date} has not finished yet")

    url = f"https://app.circleci.com/pipelines/{PROJECT_URL_PATH}/{workflow['pipeline_number']}/workflows/{workflow['id']}"
    failed = sorted(
        job["name"] for job in jobs if job["status"] not in ("success", "not_run")
    )
    print(f"Nightly {date}: {url}")
    print(f"Failed jobs: {', '.join(failed) or 'none'}")

    output(
        investigate=str(any(job["status"] != "success" for job in jobs)).lower(),
        date=date,
        url=url,
        failed=",".join(failed),
    )


if __name__ == "__main__":
    main()
