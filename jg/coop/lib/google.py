import json
import os
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_credentials(scopes) -> service_account.Credentials:
    info_json = (
        os.getenv("GOOGLE_SERVICE_ACCOUNT")
        or Path("google_service_account.json").read_text()
    )
    info = json.loads(info_json)
    credentials = service_account.Credentials.from_service_account_info(info)
    return credentials.with_scopes(scopes)


def get_client(api_name, api_version, scope):
    credentials = get_credentials(scope)
    return build(api_name, api_version, credentials=credentials, cache_discovery=False)
