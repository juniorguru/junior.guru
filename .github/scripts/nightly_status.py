"""Finds today's CircleCI nightly and tells the GitHub workflow whether Claude should investigate it"""

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import UTC, datetime


API_URL = "https://circleci.com/api/v3"
PROJECT_ID = "ecf683af-646e-4014-8483-a95ab98fa816"  # gh/juniorguru/junior.guru
PROJECT_URL_PATH = "gh/juniorguru/junior.guru"
RUNS_PAGES = 5


def get(path: str, params: dict) -> dict:
    url = f"{API_URL}{path}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def find_nightly(date: str) -> dict:
    params = {"filter[project_id]": PROJECT_ID, "page[limit]": 20}
    for _ in range(RUNS_PAGES):
        page = get("/runs", params)
        for run in page["data"]:
            if not is_scheduled_on_main(run):
                continue
            for workflow in get("/workflows", {"filter[run_id]": run["id"]})["data"]:
                attributes = workflow["attributes"]
                if attributes["name"] == "nightly" and attributes[
                    "created_at"
                ].startswith(date):
                    return {"run_number": run["attributes"]["number"], **workflow}
        if not (cursor := page.get("page", {}).get("next")):
            break
        params["page[cursor]"] = cursor
    sys.exit(f"No nightly found for {date}")


def is_scheduled_on_main(run: dict) -> bool:
    references = run["references"]
    event_source = references["trigger"]["attributes"]["event_source"]["type"]
    branch = references["event"]["attributes"].get("vcs", {}).get("branch")
    return event_source == "schedule" and branch == "main"


def output(**values: str) -> None:
    with open(os.environ.get("GITHUB_OUTPUT", "/dev/stdout"), "a") as file:
        file.writelines(f"{key}={value}\n" for key, value in values.items())


def main() -> None:
    date = datetime.now(UTC).date().isoformat()
    workflow = find_nightly(date)
    attributes = workflow["attributes"]
    if attributes["phase"] != "ended":
        sys.exit(f"Nightly for {date} has not finished yet")

    url = f"https://app.circleci.com/pipelines/{PROJECT_URL_PATH}/{workflow['run_number']}/workflows/{workflow['id']}"
    print(f"Nightly {attributes['outcome']}: {url}")
    jobs = get("/jobs", {"filter[workflow_id]": workflow["id"]})["data"]
    failed = sorted(
        job["attributes"]["name"]
        for job in jobs
        if job["attributes"]["outcome"] == "failed"
    )
    print(f"Failed jobs: {', '.join(failed) or 'none'}")

    output(
        investigate=str(attributes["outcome"] != "succeeded").lower(),
        date=date,
        url=url,
        failed=",".join(failed),
    )


if __name__ == "__main__":
    main()
