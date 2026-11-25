import csv
import email
import email.policy
import json
import os
import re
from collections.abc import Callable, Generator, Iterable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from operator import itemgetter
from pathlib import Path
from typing import Any

import httpx2
from gql import Client, gql
from gql.transport.exceptions import TransportConnectionFailed
from gql.transport.httpx import HTTPXTransport
from lxml import html
from tenacity import (
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

from jg.coop.lib import loggers
from jg.coop.lib.brand import BOT_USER_AGENT
from jg.coop.lib.cache import cache
from jg.coop.lib.imap import fetch_emails
from jg.coop.lib.retrying import retry


BROWSER_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0"

COLLECTION_NAME_RE = re.compile(r"(?P<collection_name>\w+)\([^\)]*after:\s*\$cursor")

MEMBERFUL_API_KEY = os.getenv("MEMBERFUL_API_KEY")

MEMBERFUL_EMAIL = os.getenv("MEMBERFUL_EMAIL") or "kure@junior.guru"

MEMBERFUL_PASSWORD = os.getenv("MEMBERFUL_PASSWORD")

# Mailbox where the alias Memberful sends one-time codes to forwards a copy,
# so that the sync can sign in on its own when the trusted browser expires.
MEMBERFUL_IMAP_HOST = os.getenv("MEMBERFUL_IMAP_HOST") or "imap.seznam.cz"

MEMBERFUL_IMAP_USER = os.getenv("MEMBERFUL_IMAP_USER")

MEMBERFUL_IMAP_PASSWORD = os.getenv("MEMBERFUL_IMAP_PASSWORD")

MEMBERFUL_DOMAIN = "juniorguru.memberful.com"

ONE_TIME_CODE_SENDER = "mail@memberful.com"

ONE_TIME_CODE_RE = re.compile(r"^\s*([A-Z0-9]{4,12})\s*$", re.MULTILINE)

# Tolerance for the difference between our clock and Memberful's
ONE_TIME_CODE_CLOCK_SKEW = timedelta(seconds=30)

TRUSTED_BROWSER_COOKIE = "staff_trusted_browser"

# Memberful replaces its long-lived trusted browser cookie on every sign-in and
# the previous value stops working, so all CI builds on all branches share the
# newest one through a dedicated cache, saved right after syncing, even on
# failure (see .circleci/config.yml). The cache key is a checksum of the cookie
# file, so parallel nodes which didn't sign in produce a key which already
# exists and CircleCI discards their save. Only a new cookie creates a new
# cache, which is then the newest match for the key prefix.
MEMBERFUL_TRUSTED_BROWSER_PATH = Path(
    os.getenv("MEMBERFUL_TRUSTED_BROWSER_PATH") or "~/.memberful/trusted_browser"
).expanduser()


logger = loggers.from_path(__file__)


class MemberfulAPI:
    # https://memberful.com/help/integrate/advanced/memberful-api/
    # https://juniorguru.memberful.com/api/graphql/explorer?api_user_id=52463

    def __init__(
        self,
        api_key: str | None = None,
        user_agent: str | None = None,
    ):
        self.api_key = api_key or MEMBERFUL_API_KEY
        self.user_agent = user_agent or BOT_USER_AGENT
        self._client = None

    @property
    def client(self) -> Client:
        if not self._client:
            logger.debug("Connecting")
            transport = HTTPXTransport(
                url="https://juniorguru.memberful.com/api/graphql/",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "User-Agent": self.user_agent,
                },
                transport=httpx2.HTTPTransport(verify=True, retries=3),
                timeout=httpx2.Timeout(30.0),
            )
            self._client = Client(transport=transport)
        return self._client

    def mutate(self, mutation: str, variable_values: dict) -> dict[str, Any]:
        logger.debug("Sending a mutation")
        return self.client.execute(gql(mutation), variable_values=variable_values)

    def get_nodes(
        self, query: str, variable_values: dict | None = None
    ) -> Generator[dict]:
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

    def get(self, query: str, variable_values: dict | None = None) -> list[dict]:
        return self._execute_query(query, variable_values)

    def _query(
        self, query: str, get_page_info: Callable, variable_values: dict | None = None
    ):
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
    @retry(retry=retry_if_exception_type(TransportConnectionFailed))
    def _execute_query(self, query: str, variable_values: dict) -> dict:
        logger.debug(
            f"Querying Memberful API, variable values: {json.dumps(variable_values)}"
        )
        return self.client.execute(gql(query), variable_values=variable_values)


class DownloadError(Exception):
    pass


class OneTimeCodeRequired(Exception):
    pass


class OneTimeCodeNotFound(Exception):
    pass


@dataclass
class MemberfulAuthToken:
    param: str
    value: str


class MemberfulCSV:
    def __init__(
        self,
        email: str | None = None,
        password: str | None = None,
        imap_host: str | None = None,
        imap_user: str | None = None,
        imap_password: str | None = None,
        user_agent: str | None = None,
    ):
        self.email = email or MEMBERFUL_EMAIL
        self.password = password or MEMBERFUL_PASSWORD
        self.trusted_browser_path = MEMBERFUL_TRUSTED_BROWSER_PATH
        self.trusted_browser = read_trusted_browser(self.trusted_browser_path)
        self.imap_host = imap_host or MEMBERFUL_IMAP_HOST
        self.imap_user = imap_user or MEMBERFUL_IMAP_USER
        self.imap_password = imap_password or MEMBERFUL_IMAP_PASSWORD
        self.user_agent = user_agent or BROWSER_USER_AGENT
        self._session = None
        self._auth_token = None

    @property
    def session(self) -> httpx2.Client:
        if not self._session:
            self._session, self._auth_token = self._auth()
        return self._session

    @property
    def auth_token(self) -> MemberfulAuthToken:
        if not self._auth_token:
            self._session, self._auth_token = self._auth()
        return self._auth_token

    def _auth(self) -> tuple[httpx2.Client, Any]:
        logger.debug("Logging into Memberful")
        session = create_session()
        if self.trusted_browser:
            session.cookies.set(
                TRUSTED_BROWSER_COOKIE,
                self.trusted_browser,
                domain=MEMBERFUL_DOMAIN,
            )
        since = datetime.now(UTC) - ONE_TIME_CODE_CLOCK_SKEW
        response = sign_in(session, self.email, self.password)
        response = submit_one_time_code(
            response, session, lambda: self._get_one_time_code(since)
        )
        self._store_trusted_browser(session)
        logger.debug("Parsing auth token")
        html_tree = html.fromstring(response.content)
        return session, MemberfulAuthToken(
            html_tree.cssselect('meta[name="csrf-param"]')[0].get("content"),
            html_tree.cssselect('meta[name="csrf-token"]')[0].get("content"),
        )

    def _store_trusted_browser(self, session: httpx2.Client) -> None:
        value = session.cookies.get(TRUSTED_BROWSER_COOKIE, domain=MEMBERFUL_DOMAIN)
        if value and value != self.trusted_browser:
            logger.info(
                f"Storing a new trusted browser cookie: {self.trusted_browser_path}"
            )
            write_trusted_browser(self.trusted_browser_path, value)
            self.trusted_browser = value

    def _get_one_time_code(self, since: datetime) -> str:
        logger.info("Memberful requires a one-time code, reading it from email")
        if not (self.imap_user and self.imap_password):
            raise OneTimeCodeRequired(
                "Memberful requires a one-time code to sign in. Set "
                "MEMBERFUL_IMAP_USER and MEMBERFUL_IMAP_PASSWORD, so that "
                "it can be read from email."
            )
        return self._poll_for_one_time_code(since)

    @retry(
        retry=retry_if_exception_type(OneTimeCodeNotFound),
        wait=wait_fixed(5),
        stop=stop_after_attempt(24),
    )
    def _poll_for_one_time_code(self, since: datetime) -> str:
        raw_emails = fetch_emails(
            self.imap_host,
            self.imap_user,
            self.imap_password,
            ONE_TIME_CODE_SENDER,
            (since - timedelta(days=1)).date(),
        )
        if code := select_one_time_code(raw_emails, since):
            return code
        raise OneTimeCodeNotFound(f"No one-time code email since {since}")

    def download_csv(self, *args, **kwargs) -> csv.DictReader:
        return csv.DictReader(self._download_csv(*args, **kwargs).splitlines())

    @cache(expire=timedelta(hours=1), ignore=(0,), tag="memberful-csv")
    @retry(
        retry=(
            retry_if_exception_type(httpx2.HTTPStatusError)
            | retry_if_exception_type(httpx2.ConnectError)
        ),
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
            follow_redirects=False,
        )
        # The POST 303-redirects to the created export. Unlike requests,
        # httpx2's raise_for_status() treats an unfollowed redirect as an error,
        # so only raise on a genuine 4xx/5xx here.
        if response.is_error:
            response.raise_for_status()

        location_url = response.headers.get("Location") or None
        if location_url is None:
            logger.debug("Parsing export ID from HTML")
            html_tree = html.fromstring(response.content)
            export_id = parse_export_id(html_tree)
        else:
            logger.debug("Parsing export ID from Location header")
            export_id = int(location_url.rstrip("/").split("/")[-1])

        # The file always downloads from /admin/csv_exports/{id}/download,
        # regardless of which endpoint created the export. E.g. POST to
        # /admin/members/exports redirects to /admin/members/exports/{id},
        # but the actual CSV lives under /admin/csv_exports/{id}/download.
        download_url = (
            f"https://juniorguru.memberful.com/admin/csv_exports/{export_id}/download"
        )

        logger.debug(f"Polling: {download_url}")
        return self._poll_for_csv(download_url)

    @retry(
        retry=retry_if_exception_type(httpx2.HTTPStatusError),
        wait=wait_fixed(5),
        stop=stop_after_attempt(10),
    )
    def _poll_for_csv(self, download_url: str) -> str:
        response = self.session.get(download_url)
        response.raise_for_status()
        return response.content.decode("utf-8")


def read_trusted_browser(path: Path) -> str | None:
    try:
        return path.read_text().strip() or None
    except FileNotFoundError:
        return None


def write_trusted_browser(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value)


def create_session() -> httpx2.Client:
    return httpx2.Client(
        follow_redirects=True, headers={"User-Agent": BROWSER_USER_AGENT}
    )


def sign_in(session: httpx2.Client, email: str, password: str) -> httpx2.Response:
    response = session.get(f"https://{MEMBERFUL_DOMAIN}/admin/auth/sign_in")
    response.raise_for_status()
    return submit_form(response, session, {"email": email, "password": password})


def submit_one_time_code(
    response: httpx2.Response, session: httpx2.Client, get_code: Callable[[], str]
) -> httpx2.Response:
    """Submits a one-time code if Memberful asks for one after signing in"""
    if not is_one_time_code_url(str(response.url)):
        return response
    response = submit_form(response, session, {"otp": get_code()})
    if is_one_time_code_url(str(response.url)):
        raise OneTimeCodeRequired("The one-time code was not accepted")
    return response


def submit_form(
    response: httpx2.Response, session: httpx2.Client, values: dict[str, str]
) -> httpx2.Response:
    html_tree = html.fromstring(response.content)
    html_tree.make_links_absolute(str(response.url))
    form = html_tree.forms[0]
    for name, value in values.items():
        form.fields[name] = value
    response = session.post(form.action, data=dict(form.form_values()))
    response.raise_for_status()
    return response


def select_one_time_code(raw_emails: Iterable[bytes], since: datetime) -> str | None:
    """Returns the code from the newest one-time code email sent at or after the given time"""
    parsed = filter(None, map(parse_one_time_code_email, raw_emails))
    if candidates := [item for item in parsed if item[0] >= since]:
        return max(candidates, key=itemgetter(0))[1]
    return None


def parse_one_time_code_email(raw_email: bytes) -> tuple[datetime, str] | None:
    """Returns the time a Memberful one-time code email was sent and the code in it"""
    message = email.message_from_bytes(raw_email, policy=email.policy.default)
    addresses = message["From"].addresses if message["From"] else ()
    if ONE_TIME_CODE_SENDER not in [address.addr_spec for address in addresses]:
        return None
    body = message.get_body(preferencelist=("plain",))
    if body and (match := ONE_TIME_CODE_RE.search(body.get_content())):
        return message["Date"].datetime, match.group(1)
    return None


def memberful_url(account_id: int | str) -> str:
    if not account_id:
        raise ValueError(f"{account_id}")
    return f"https://juniorguru.memberful.com/admin/members/{account_id}/"


def is_one_time_code_url(url: str) -> bool:
    return "/admin/auth/magic_link" in url


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
    return re.search(r"\bčlenství\sv\sklubu\b", plan["name"], re.IGNORECASE) is not None


def timestamp_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=UTC).replace(tzinfo=None)


def timestamp_to_date(timestamp: int) -> date:
    return timestamp_to_datetime(timestamp).date()
