import base64
import os

import httpx


BASE_URL = "https://app.fakturoid.cz/api/v3/accounts/honzajavorek"

USER_AGENT = "JuniorGuruBot (honza@junior.guru; +https://junior.guru)"

CLIENT_ID = os.getenv("FAKTUROID_CLIENT_ID")

CLIENT_SECRET = os.getenv("FAKTUROID_CLIENT_SECRET")


def auth(
    client_id: str | None = None,
    client_secret: str | None = None,
    user_agent: str | None = None,
) -> str:
    client_id = client_id or CLIENT_ID
    client_secret = client_secret or CLIENT_SECRET
    user_agent = user_agent or USER_AGENT

    credentials = f"{client_id}:{client_secret}"
    credentials_base64 = base64.b64encode(credentials.encode()).decode()
    response = httpx.post(
        "https://app.fakturoid.cz/api/v3/oauth/token",
        headers={
            "Accept": "application/json",
            "User-Agent": user_agent,
            "Authorization": f"Basic {credentials_base64}",
        },
        json=dict(grant_type="client_credentials"),
        follow_redirects=True,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def get_client(
    token: str, base_url: str | None = None, user_agent: str | None = None
) -> httpx.Client:
    base_url = (base_url or BASE_URL).rstrip("/")
    user_agent = user_agent or USER_AGENT
    return httpx.Client(
        base_url=base_url,
        headers={"User-Agent": user_agent, "Authorization": f"Bearer {token}"},
        follow_redirects=True,
    )
