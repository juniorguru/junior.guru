import os
from datetime import date
from enum import StrEnum
from typing import AsyncGenerator, Self, TypeVar

import httpx

from jg.coop.lib import loggers, mutations


T = TypeVar("T")

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


class ButtondownError(Exception):
    def __init__(
        self,
        message: str,
        http_code: int | None = None,
        code: str | None = None,
        metadata: dict | None = None,
        url: str | None = None,
    ):
        super().__init__(message)
        self.http_code = http_code
        self.code = code
        self.metadata = metadata or {}


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

    async def _request(self, method: str, url: str, **kwargs) -> dict:
        try:
            response = await self._client.request(method.lower(), url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            exc_data = e.response.json()
            raise ButtondownError(
                f"{exc_data['detail']} – {e.request.method} {e.request.url}",
                http_code=e.response.status_code,
                code=exc_data.get("code"),
                metadata=exc_data.get("metadata"),
            ) from e

    async def get_emails_before(self, before_date: date) -> AsyncGenerator[dict, None]:
        next_url = f"emails?publish_date__end={before_date}"
        while next_url:
            logger.debug(f"Fetching emails: {next_url}")
            data = await self._request("GET", next_url)
            for item in data["results"]:
                yield item
            next_url = data["next"]

    async def get_emails_since(self, since_date: date) -> dict:
        return await self._request(
            "GET", "emails", params={"publish_date__start": since_date.isoformat()}
        )

    @mutations.mutates_buttondown()
    async def update_email(self, email_id: str, email_data: dict) -> None:
        return await self._request("PATCH", f"emails/{email_id}", json=email_data)

    @mutations.mutates_buttondown()
    async def create_draft(self, email_data: dict) -> None:
        return await self._request("POST", "emails", json=email_data)

    async def count_subscribers(self) -> int:
        data = await self._request("GET", "subscribers", params={"type": "regular"})
        return data["count"]

    @mutations.mutates_buttondown()
    async def add_subscriber(self, email: str, tags=set[SubscriberSource]) -> dict:
        logger.debug(f"Adding subscriber {email} with tags {tags}")
        subscriber_type = get_subscriber_type(tags)
        try:
            subscriber = await self._request("GET", f"subscribers/{email}")
        except ButtondownError as e:
            if e.http_code == 404:
                logger.debug(f"Creating subscriber {email}")
                logger.debug(f"Subscriber {email} classified as {subscriber_type!r}")
                return await self._request(
                    "POST",
                    "subscribers",
                    json={
                        "email_address": email,
                        "tags": list(tags),
                        "type": subscriber_type,
                    },
                )
            raise

        if subscriber_type == "regular" and subscriber["type"] != "regular":
            logger.warning(
                f"Subscriber {email} has type {subscriber['type']!r}, "
                f"but should be {subscriber_type!r}"
            )

        existing_tags = set(subscriber.get("tags", []))
        if existing_tags == tags:
            logger.debug(f"Subscriber {email} up-to-date, skipping")
            return subscriber

        logger.debug(f"Updating subscriber {email}, tags: {existing_tags} → {tags}")
        return await self._request(
            "PATCH", f"subscribers/{email}", json={"tags": list(existing_tags | tags)}
        )


def get_subscriber_type(tags: set[SubscriberSource]) -> str:
    return "unactivated" if tags == {SubscriberSource.MEMBERFUL} else "regular"
