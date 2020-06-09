import json
from pathlib import Path

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SERVICE_ACCOUNT_PATH = Path(__file__).parent / 'google_service_account.json'


def get_credentials(scope):
    service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT') or SERVICE_ACCOUNT_PATH.read_text()
    service_account = json.loads(service_account_json)
    return ServiceAccountCredentials.from_json_keyfile_dict(service_account, scope)


def get_client(name, version, scope):
    return build(name, version, credentials=get_credentials(scope))
