import os
from datetime import date
from enum import StrEnum
from typing import Self

import httpx

from jg.coop.lib import loggers, mutations


BUTTONDOWN_API_KEY = os.getenv("BUTTONDOWN_API_KEY")


logger = loggers.from_path(__file__)


class SubscriberSource(StrEnum):
    ECOMAIL = "ecomail"
    MAILCHIMP = "mailchimp"
    MEMBERFUL = "memberful"


class SubscriberErrorCode(StrEnum):
    EMAIL_ALREADY_EXISTS = "email_already_exists"
    EMAIL_BLOCKED = "email_blocked"
    EMAIL_INVALID = "email_invalid"
    IP_ADDRESS_SPAMMY = "ip_address_spammy"
    METADATA_INVALID = "metadata_invalid"
    RATE_LIMITED = "rate_limited"
    SUBSCRIBER_ALREADY_EXISTS = "subscriber_already_exists"
    SUBSCRIBER_BLOCKED = "subscriber_blocked"
    SUBSCRIBER_SUPPRESSED = "subscriber_suppressed"
    TAG_INVALID = "tag_invalid"


class ButtondownAPI:

    def __init__(self, token: str | None = None) -> None:
        self.token = token or BUTTONDOWN_API_KEY
        self._client = None

    async def __aenter__(self) -> Self:
        self._client = httpx.AsyncClient(
            base_url="https://api.buttondown.com/v1/",
            headers={"Authorization": f"Token {self.token}"},
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
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

    # @mutations.mutates_buttondown()
    async def add_subscriber(self, email: str, tags=set[SubscriberSource]) -> None:
        # first get subscriber by email, check if all is ok
        # if not, either update tags or create
        try:
            response = await self._client.get(f"subscribers/{email}")
            response.raise_for_status()
            subscriber = response.json()
            existing_tags = set(subscriber.get("tags", []))
            print(existing_tags)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                response = await self._client.post(
                    "subscribers",
                    json={
                        "email_address": email,
                        "tags": list(tags),
                        "type": "regular",
                    },
                )
                response.raise_for_status()
            else:
                raise

        # response = await self._client.post(
        #     "subscribers",
        #     json={"email_address": email, "tags": list(tags), "type": "regular"},
        # )
        # try:
        #     response.raise_for_status()
        # except httpx.HTTPStatusError as e:
        #     if e.response.status_code != 400:
        #         raise
        #     error_data = e.response.json()
        #     error_code = error_data.get("code")
        #     if error_code == SubscriberErrorCode.EMAIL_ALREADY_EXISTS:
        #         subscriber_id = error_data["metadata"]["subscriber_id"]
        #         raise EmailAreadyExistsError(subscriber_id) from e
        # return response.json()
