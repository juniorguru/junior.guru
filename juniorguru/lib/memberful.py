import csv
import json
import logging
import os
import re
from datetime import timedelta
from typing import Any, Callable, Generator
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

from juniorguru.lib import loggers
from juniorguru.lib.cache import cache


USER_AGENT = "JuniorGuruBot (+https://junior.guru)"

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
    ):
        self.api_key = api_key or MEMBERFUL_API_KEY
        self._client = None

    @property
    def client(self) -> Client:
        if not self._client:
            logger.debug("Connecting")
            transport = RequestsHTTPTransport(
                url="https://juniorguru.memberful.com/api/graphql/",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "User-Agent": USER_AGENT,
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

    @cache(expire=timedelta(days=1), ignore=(0,), tag="memberful-api")
    def _execute_query(self, query: str, variable_values: dict) -> dict:
        logger.debug(
            f"Querying Memberful API, variable values: {json.dumps(variable_values)}"
        )
        return self.client.execute(gql(query), variable_values=variable_values)


class DownloadError(Exception):
    pass


class MemberfulCSV:
    def __init__(
        self,
        email: str = None,
        password: str = None,
    ):
        self.email = email or MEMBERFUL_EMAIL
        self.password = password or MEMBERFUL_PASSWORD
        self._session = None
        self._csrf_token = None

    @property
    def session(self) -> requests.Session:
        if not self._session:
            self._session, self._csrf_token = self._auth()
        return self._session

    @property
    def csrf_token(self) -> str:
        if not self._csrf_token:
            self._session, self._csrf_token = self._auth()
        return self._csrf_token

    def _auth(self) -> tuple[requests.Session, Any]:
        logger.debug("Logging into Memberful")
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})
        response = session.get("https://juniorguru.memberful.com/admin/auth/sign_in")
        response.raise_for_status()
        html_tree = html.fromstring(response.content)
        html_tree.make_links_absolute(response.url)
        form = html_tree.forms[0]
        form.fields["email"] = self.email
        form.fields["password"] = self.password
        response = session.post(form.action, data=form.form_values())
        response.raise_for_status()
        html_tree = html.fromstring(response.content)
        csrf_token = html_tree.cssselect('meta[name="csrf-token"]')[0].get("content")
        logger.debug("Success!")
        return session, csrf_token

    def download_csv(self, params: dict) -> csv.DictReader:
        return csv.DictReader(self._download_csv(params).splitlines())

    @cache(expire=timedelta(days=1), ignore=(0,), tag="memberful-csv")
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
    def _download_csv(self, params: dict) -> str:
        url = f"https://juniorguru.memberful.com/admin/csv_exports?{urlencode(params)}"
        logger.debug(f"Downloading CSV export: {url}")
        response = self.session.post(
            url, allow_redirects=False, headers={"X-CSRF-Token": self.csrf_token}
        )
        response.raise_for_status()
        download_url = f"{response.headers['Location']}/download"
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
