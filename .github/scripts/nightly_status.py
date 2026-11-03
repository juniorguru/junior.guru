"""Finds today's CircleCI nightly and tells the GitHub workflow whether Claude should investigate it"""

import json
import os
import sys
import urllib.request
from datetime import UTC, datetime


API_URL = "https://circleci.com/api"
PROJECT_URL_PATH = "gh/juniorguru/junior.guru"


def get(path: str) -> dict | list:
    request = urllib.request.Request(
        f"{API_URL}{path}", headers={"Accept": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def find_nightly(date: str) -> dict:
    # Unauthenticated GET /pipeline/{id}/workflow returns 404, so workflow IDs
    # are taken from the API v1.1 list of recent builds on main
    builds = get(f"/v1.1/project/{PROJECT_URL_PATH}/tree/main?limit=100&shallow=true")
    workflow_ids = {
        build["workflows"]["workflow_id"]: None
        for build in builds
        if (build.get("workflows") or {}).get("workflow_name") == "nightly"
    }
    for workflow_id in workflow_ids:
        workflow = get(f"/v2/workflow/{workflow_id}")
        if workflow["created_at"].startswith(date):
            return workflow
    sys.exit(f"No nightly found for {date}")


def output(**values: str) -> None:
    with open(os.environ.get("GITHUB_OUTPUT", "/dev/stdout"), "a") as file:
        file.writelines(f"{key}={value}\n" for key, value in values.items())


def main() -> None:
    date = datetime.now(UTC).date().isoformat()
    workflow = find_nightly(date)
    if workflow["status"] in ("running", "on_hold"):
        sys.exit(f"Nightly for {date} has not finished yet")

    url = f"https://app.circleci.com/pipelines/{PROJECT_URL_PATH}/{workflow['pipeline_number']}/workflows/{workflow['id']}"
    print(f"Nightly {workflow['status']}: {url}")
    jobs = get(f"/v2/workflow/{workflow['id']}/job")["items"]
    failed = sorted(job["name"] for job in jobs if job["status"] == "failed")
    print(f"Failed jobs: {', '.join(failed) or 'none'}")

    output(
        investigate=str(workflow["status"] != "success").lower(),
        date=date,
        url=url,
        failed=",".join(failed),
    )


if __name__ == "__main__":
    main()
