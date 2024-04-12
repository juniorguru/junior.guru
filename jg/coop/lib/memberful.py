import csv
from dataclasses import dataclass
import json
import logging
import os
from pathlib import Path
import re
from datetime import timedelta
from typing import Any, Callable, Generator, Self
from urllib.parse import urlencode

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

MEMBERFUL_API_KEY = os.environ.get("MEMBERFUL_API_KEY")

MEMBERFUL_EMAIL = os.environ.get("MEMBERFUL_EMAIL", "kure@junior.guru")

MEMBERFUL_PASSWORD = os.environ.get("MEMBERFUL_PASSWORD")


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

        declared_count = None
        nodes_count = 0
        for result in self._query(
            query,
            lambda result: result[collection_name]["pageInfo"],
            variable_values=variable_values,
        ):
            # save total count so we can later check if we got all the nodes
            count = result[collection_name]["totalCount"]
            if declared_count is None:
                logger.debug(f"Expecting {count} nodes")
                declared_count = count
            if declared_count != count:
                raise ValueError(
                    f"Memberful API suddenly declares different total count: {count} (≠ {declared_count})"
                )

            # yield and count nodes
            for edge in result[collection_name]["edges"]:
                yield edge["node"]
                nodes_count += 1

        # check if we got all the nodes
        if declared_count != nodes_count:
            raise ValueError(
                f"Memberful API returned {nodes_count} nodes instead of {declared_count}"
            )

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
    return f"https://juniorguru.memberful.com/admin/members/{account_id}/"


def parse_export_id(html_tree: html.HtmlElement) -> int:
    html_element = html_tree.cssselect("*[data-auto-refreshable-url-value]")[0]
    refreshable_url = html_element.get("data-auto-refreshable-url-value")

    # refreshable_url is something like /admin/members/exports/68746
    return int(refreshable_url.split("/")[-1])
