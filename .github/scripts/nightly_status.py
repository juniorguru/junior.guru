"""Finds today's CircleCI nightly and tells the GitHub workflow whether Claude should investigate it."""

import json
import os
import sys
import time
import urllib.request
from datetime import UTC, datetime


API = "https://circleci.com/api/v2"
PROJECT = "gh/juniorguru/junior.guru"
# Failures in these jobs are intentional reminders, not breakages
EXPECTED_FAILURES = {"check-sponsors"}
POLL_INTERVAL = 5 * 60
POLL_LIMIT = 20 * 60


def get(path: str) -> dict:
    with urllib.request.urlopen(f"{API}{path}", timeout=30) as response:
        return json.load(response)


def find_nightly(date: str) -> dict | None:
    pipelines = get(f"/project/{PROJECT}/pipeline?branch=main")["items"]
    for pipeline in pipelines:
        if pipeline["trigger"]["type"] != "schedule":
            continue
        for workflow in get(f"/pipeline/{pipeline['id']}/workflow")["items"]:
            if workflow["name"] == "nightly" and workflow["created_at"].startswith(
                date
            ):
                return {"pipeline_number": pipeline["number"], **workflow}
    return None


def output(**values: str) -> None:
    with open(os.environ.get("GITHUB_OUTPUT", "/dev/stdout"), "a") as file:
        file.writelines(f"{key}={value}\n" for key, value in values.items())


def main() -> None:
    date = datetime.now(UTC).date().isoformat()
    started = time.monotonic()
    while True:
        workflow = find_nightly(date)
        if workflow and workflow["status"] not in ("running", "on_hold"):
            break
        if time.monotonic() - started > POLL_LIMIT:
            print(f"Nightly for {date} not finished: {workflow and workflow['status']}")
            output(investigate="false")
            return
        print(f"Waiting for nightly for {date}: {workflow and workflow['status']}")
        time.sleep(POLL_INTERVAL)

    url = f"https://app.circleci.com/pipelines/{PROJECT}/{workflow['pipeline_number']}/workflows/{workflow['id']}"
    print(f"Nightly {workflow['status']}: {url}")
    jobs = get(f"/workflow/{workflow['id']}/job")["items"]
    failed = sorted(job["name"] for job in jobs if job["status"] == "failed")
    print(f"Failed jobs: {', '.join(failed) or 'none'}")

    unexpected = set(failed) - EXPECTED_FAILURES
    investigate = workflow["status"] != "success" and (unexpected or not failed)
    output(
        investigate=str(bool(investigate)).lower(),
        date=date,
        url=url,
        failed=",".join(failed),
    )


if __name__ == "__main__":
    sys.exit(main())
