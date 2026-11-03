import httpx2


API_URL = "https://circleci.com/api/v3"

PROJECT_ID = "ecf683af-646e-4014-8483-a95ab98fa816"  # gh/juniorguru/junior.guru

WEB_URL = "https://app.circleci.com/pipelines/github/juniorguru/junior.guru"


def create_client(api_key: str | None) -> httpx2.Client:
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    return httpx2.Client(
        base_url=API_URL, headers=headers, timeout=30, follow_redirects=True
    )


def get_data(client: httpx2.Client, path: str, params: dict | None = None) -> list:
    response = client.get(path, params=params)
    response.raise_for_status()
    return response.json()["data"]


def get_workflow_url(run_number: int, workflow_id: str) -> str:
    return f"{WEB_URL}/{run_number}/workflows/{workflow_id}"
