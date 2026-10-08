"""Finds today's CircleCI nightly and tells the GitHub workflow whether Claude should investigate it"""

import json
import os
import sys
import urllib.request
from datetime import UTC, datetime


API_URL = "https://circleci.com/api/v2"
PROJECT_URL_PATH = "gh/juniorguru/junior.guru"


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
                return {"pipeline_number": pipeline["number"], **workflow}
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
    jobs = get(f"/workflow/{workflow['id']}/job")["items"]
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
