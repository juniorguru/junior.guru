import os
import json
import datetime
from pathlib import Path
from operator import itemgetter

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from .sheets import coerce_record
from ..models import db, Job


def main():
    google_service_account_path = Path(__file__).parent / 'google_service_account.json'
    google_service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT') or google_service_account_path.read_text()
    google_service_account = json.loads(google_service_account_json)
    google_scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_service_account, google_scope)

    doc_key = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'
    doc = gspread.authorize(credentials).open_by_key(doc_key)
    records = doc.worksheet('jobs').get_all_records(default_blank=None)

    with db:
        Job.drop_table()
        Job.create_table()

        for record in records:
            Job.create(**coerce_record(record))


if __name__ == '__main__':
    main()
