import csv
import json
import logging
import os
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Any, Callable, Generator

import requests
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from lxml import html
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
    wait_random_exponential,
)

from jg.coop.lib import loggers
from jg.coop.lib.cache import cache


BOT_USER_AGENT = "JuniorGuruBot (+https://junior.guru)"

BROWSER_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0"

COLLECTION_NAME_RE = re.compile(r"(?P<collection_name>\w+)\([^\)]*after:\s*\$cursor")

MEMBERFUL_API_KEY = os.getenv("MEMBERFUL_API_KEY")

MEMBERFUL_EMAIL = os.getenv("MEMBERFUL_EMAIL") or "kure@junior.guru"

MEMBERFUL_PASSWORD = os.getenv("MEMBERFUL_PASSWORD")


logger = loggers.from_path(__file__)


class MemberfulAPI:
    # https://memberful.com/help/integrate/advanced/memberful-api/
    # https://juniorguru.memberful.com/api/graphql/explorer?api_user_id=52463

    def __init__(
        self,
        api_key: str = None,
        user_agent: str | None = None,
    ):
        self.api_key = api_key or MEMBERFUL_API_KEY
        self.user_agent = user_agent or BOT_USER_AGENT
        self._client = None

    @property
    def client(self) -> Client:
        if not self._client:
            logger.debug("Connecting")
            transport = RequestsHTTPTransport(
                url="https://juniorguru.memberful.com/api/graphql/",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "User-Agent": self.user_agent,
                },
                verify=True,
                retries=3,
            )
            self._client = Client(transport=transport)
        return self._client

    def mutate(self, mutation: str, variable_values: dict) -> dict[str, Any]:
        logger.debug("Sending a mutation")
        return self.client.execute(gql(mutation), variable_values=variable_values)

    def get_nodes(
        self, query: str, variable_values: dict = None
    ) -> Generator[dict, None, None]:
        if match := COLLECTION_NAME_RE.search(query):
            collection_name = match.group("collection_name")
        else:
            raise ValueError("Could not parse collection name")
        for result in self._query(
            query,
            lambda result: result[collection_name]["pageInfo"],
            variable_values=variable_values,
        ):
            for edge in result[collection_name]["edges"]:
                yield edge["node"]

    def get(self, query: str, variable_values: dict = None) -> list[dict]:
        return self._execute_query(query, variable_values)

    def _query(self, query: str, get_page_info: Callable, variable_values: dict = None):
        variable_values = variable_values or {}
        cursor = ""
        n = 0
        while cursor is not None:
            logger.debug(f"Sending a query with cursor {cursor!r}")
            result = self._execute_query(query, dict(cursor=cursor, **variable_values))
            yield result
            n += 1
            page_info = get_page_info(result)
            if page_info["hasNextPage"]:
                cursor = page_info["endCursor"]
            else:
                cursor = None

    @cache(expire=timedelta(hours=1), ignore=(0,), tag="memberful-api")
    def _execute_query(self, query: str, variable_values: dict) -> dict:
        logger.debug(
            f"Querying Memberful API, variable values: {json.dumps(variable_values)}"
        )
        return self.client.execute(gql(query), variable_values=variable_values)


class DownloadError(Exception):
    pass


@dataclass
class MemberfulAuthToken:
    param: str
    value: str


class MemberfulCSV:
    def __init__(
        self,
        email: str = None,
        password: str = None,
        user_agent: str | None = None,
    ):
        self.email = email or MEMBERFUL_EMAIL
        self.password = password or MEMBERFUL_PASSWORD
        self.user_agent = user_agent or BROWSER_USER_AGENT
        self._session = None
        self._auth_token = None

    @property
    def session(self) -> requests.Session:
        if not self._session:
            self._session, self._auth_token = self._auth()
        return self._session

    @property
    def auth_token(self) -> MemberfulAuthToken:
        if not self._auth_token:
            self._session, self._auth_token = self._auth()
        return self._auth_token

    def _auth(self) -> tuple[requests.Session, Any]:
        logger.debug("Logging into Memberful")
        session = requests.Session()
        session.headers.update({"User-Agent": BROWSER_USER_AGENT})
        response = session.get("https://juniorguru.memberful.com/admin/auth/sign_in")
        response.raise_for_status()
        html_tree = html.fromstring(response.content)
        html_tree.make_links_absolute(response.url)
        form = html_tree.forms[0]
        form.fields["email"] = self.email
        form.fields["password"] = self.password
        response = session.post(form.action, data=form.form_values())
        response.raise_for_status()
        logger.debug("Parsing auth token")
        html_tree = html.fromstring(response.content)
        return session, MemberfulAuthToken(
            html_tree.cssselect('meta[name="csrf-param"]')[0].get("content"),
            html_tree.cssselect('meta[name="csrf-token"]')[0].get("content"),
        )

    def download_csv(self, *args, **kwargs) -> csv.DictReader:
        return csv.DictReader(self._download_csv(*args, **kwargs).splitlines())

    @cache(expire=timedelta(hours=1), ignore=(0,), tag="memberful-csv")
    @retry(
        retry=(
            retry_if_exception_type(requests.exceptions.HTTPError)
            | retry_if_exception_type(requests.exceptions.ConnectionError)
        ),
        wait=wait_random_exponential(max=60),
        stop=stop_after_attempt(3),
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def _download_csv(
        self,
        path: str,
        url_params: dict[str, str] | None = None,
        form_params: dict[str, str] | None = None,
    ) -> str:
        logger.debug(f"Downloading CSV export: {path}")
        response = self.session.post(
            f"https://juniorguru.memberful.com/{path.strip('/')}",
            params=url_params or {},
            headers={
                "User-Agent": BROWSER_USER_AGENT,
                "X-CSRF-Token": self.auth_token.value,
            },
            data={self.auth_token.param: self.auth_token.value} | (form_params or {}),
        )
        response.raise_for_status()

        location_url = response.headers.get("Location") or None
        if location_url is None:
            logger.debug("Parsing download URL from HTML")
            html_tree = html.fromstring(response.content)
            export_id = parse_export_id(html_tree)
            download_url = f"https://juniorguru.memberful.com/admin/csv_exports/{export_id}/download"
        else:
            logger.debug("Using Location header for download URL")
            download_url = f"{location_url}/download"

        logger.debug(f"Polling: {download_url}")
        return self._poll_for_csv(download_url)

    @retry(
        retry=retry_if_exception_type(requests.exceptions.HTTPError),
        wait=wait_fixed(5),
        stop=stop_after_attempt(10),
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.DEBUG),
    )
    def _poll_for_csv(self, download_url: str) -> str:
        response = self.session.get(download_url)
        response.raise_for_status()
        return response.content.decode("utf-8")


def memberful_url(account_id: int | str) -> str:
    if not account_id:
        raise ValueError(f"{account_id}")
    return f"https://juniorguru.memberful.com/admin/members/{account_id}/"


def parse_export_id(html_tree: html.HtmlElement) -> int:
    html_element = html_tree.cssselect("*[data-auto-refreshable-url-value]")[0]
    refreshable_url = html_element.get("data-auto-refreshable-url-value")

    # refreshable_url is something like /admin/members/exports/68746
    return int(refreshable_url.split("/")[-1])


def from_cents(cents: int) -> int:
    return int(cents / 100)


def parse_tier_name(plan_name: str) -> str:
    if match := re.search(r"^Tarif „([^“]+)“$", plan_name):
        return match.group(1)
    raise ValueError(f"Invalid plan name: {plan_name!r}")


def is_public_plan(plan: dict) -> bool:
    return plan["forSale"]


def is_sponsor_plan(plan: dict) -> bool:
    try:
        parse_tier_name(plan["name"])
    except ValueError:
        return False
    return True


def is_partner_plan(plan: dict) -> bool:
    return not (is_individual_plan(plan) or is_sponsor_plan(plan))


def is_individual_plan(plan: dict) -> bool:
    return re.search(r"\bčlenství\sv\sklubu\b", plan["name"], re.I) is not None


def timestamp_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).replace(tzinfo=None)


def timestamp_to_date(timestamp: int) -> date:
    return timestamp_to_datetime(timestamp).date()
