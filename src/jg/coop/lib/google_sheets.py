import logging

import gspread
from requests.exceptions import ConnectionError, Timeout
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from jg.coop.lib import loggers
from jg.coop.lib.google_api import get_credentials


logger = loggers.from_path(__file__)


def is_retryable_api_error(exc: Exception) -> bool:
    return isinstance(exc, gspread.exceptions.APIError) and exc.code in (429, 500, 503)


@retry(
    retry=(
        retry_if_exception(is_retryable_api_error)
        | retry_if_exception_type(ConnectionError)
        | retry_if_exception_type(Timeout)
    ),
    wait=wait_random_exponential(max=60),
    stop=stop_after_attempt(5),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def get(doc_key, sheet_name):
    credentials = get_credentials(
        [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
    )
    doc = gspread.authorize(credentials).open_by_key(doc_key)
    return doc.worksheet(sheet_name)


def download(sheet):
    return sheet.get_all_records(default_blank=None)
