import os
from datetime import date
from typing import Self

import httpx

from jg.coop.lib import loggers, mutations


BUTTONDOWN_API_KEY = os.getenv("BUTTONDOWN_API_KEY")


logger = loggers.from_path(__file__)


class ButtondownAPI:
    def __init__(self, token: str | None = None):
        self.token = token or BUTTONDOWN_API_KEY
        self._client = None

    async def __aenter__(self) -> Self:
        self._client = httpx.AsyncClient(
            base_url="https://api.buttondown.com/v1/",
            headers={"Authorization": f"Token {self.token}"},
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    async def get_emails_since(self, since_date: date) -> dict:
        response = await self._client.get(
            "emails", params={"creation_date__start": since_date.isoformat()}
        )
        response.raise_for_status()
        return response.json()

    @mutations.mutates_buttondown()
    async def create_draft(self, email_data: dict) -> None:
        response = await self._client.post("emails", json=email_data)
        response.raise_for_status()
        return response.json()
