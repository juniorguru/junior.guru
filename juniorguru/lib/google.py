import json
import os
from pathlib import Path

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SERVICE_ACCOUNT_PATH = Path(__file__).parent.parent / 'google_service_account.json'


def get_credentials(scope):
    service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT') or SERVICE_ACCOUNT_PATH.read_text()
    service_account = json.loads(service_account_json)
    return ServiceAccountCredentials.from_json_keyfile_dict(service_account, scope)


def get_client(api_name, api_version, scope):
    credentials = get_credentials(scope)
    return build(api_name, api_version, credentials=credentials)
