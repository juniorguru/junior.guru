import functools
import os
from datetime import date
from enum import StrEnum
from typing import Any, Awaitable, Callable, Self, TypeVar

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
        code: str | None = None,
        metadata: dict | None = None,
        url: str | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.metadata = metadata or {}


def convert_http_exceptions(
    fn: Callable[..., Awaitable[T]],
) -> Callable[..., Awaitable[T]]:
    @functools.wraps(fn)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return await fn(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            exc_data = e.response.json()
            raise ButtondownError(
                f"{exc_data['detail']} – {e.request.method} {e.request.url}",
                code=exc_data.get("code"),
                metadata=exc_data.get("metadata"),
            ) from e

    return wrapper


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

    @convert_http_exceptions
    async def get_emails_since(self, since_date: date) -> dict:
        response = await self._client.get(
            "emails", params={"creation_date__start": since_date.isoformat()}
        )
        response.raise_for_status()
        return response.json()

    @mutations.mutates_buttondown()
    @convert_http_exceptions
    async def create_draft(self, email_data: dict) -> None:
        response = await self._client.post("emails", json=email_data)
        response.raise_for_status()
        return response.json()

    async def count_subscribers(self) -> int:
        response = await self._client.get("subscribers", params={"type": "regular"})
        response.raise_for_status()
        data = response.json()
        return data["count"]

    @mutations.mutates_buttondown()
    @convert_http_exceptions
    async def add_subscriber(self, email: str, tags=set[SubscriberSource]) -> dict:
        logger.debug(f"Adding subscriber {email} with tags {tags}")
        subscriber_type = get_subscriber_type(tags)
        try:
            response = await self._client.get(f"subscribers/{email}")
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.debug(f"Creating subscriber {email}")
                logger.debug(f"Subscriber {email} classified as {subscriber_type!r}")
                response = await self._client.post(
                    "subscribers",
                    json={
                        "email_address": email,
                        "tags": list(tags),
                        "type": subscriber_type,
                    },
                )
                response.raise_for_status()
                return response.json()
            raise

        subscriber = response.json()
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
        response = await self._client.patch(
            f"subscribers/{email}", json={"tags": list(existing_tags | tags)}
        )
        response.raise_for_status()
        return response.json()


def get_subscriber_type(tags: set[SubscriberSource]) -> str:
    return "unactivated" if tags == {SubscriberSource.MEMBERFUL} else "regular"
