from collections.abc import Generator

import httpx2


API_URL = "https://circleci.com/api/v3"

PROJECT_ID = "ecf683af-646e-4014-8483-a95ab98fa816"  # gh/juniorguru/junior.guru

PAGE_LIMIT = 20  # maximum allowed by the API

WEB_URL = "https://app.circleci.com/pipelines/github/juniorguru/junior.guru"


def create_client(api_key: str | None) -> httpx2.Client:
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    return httpx2.Client(
        base_url=API_URL, headers=headers, timeout=30, follow_redirects=True
    )


def get_data(
    client: httpx2.Client, path: str, params: dict | None = None
) -> Generator[dict]:
    """Yields items of a list endpoint, following pagination"""
    params = dict(params or {}, **{"page[limit]": PAGE_LIMIT})
    while True:
        response = client.get(path, params=params)
        response.raise_for_status()
        payload = response.json()
        yield from payload["data"]
        if not (cursor := (payload.get("page") or {}).get("next")):
            break
        params["page[cursor]"] = cursor


def get_workflow_url(run_number: int, workflow_id: str) -> str:
    return f"{WEB_URL}/{run_number}/workflows/{workflow_id}"
