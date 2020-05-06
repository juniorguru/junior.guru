import datetime
import json
import os
import shutil
import subprocess
from multiprocessing import Pool
from operator import itemgetter
from pathlib import Path

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from juniorguru.fetch.sheets import coerce_record
from juniorguru.models import Job, JobDropped, JobError, db


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
        for model in [Job, JobError, JobDropped]:
            model.drop_table()
            model.create_table()

        for record in records:
            Job.create(**coerce_record(record))

    Pool().map(run_spider, [
        'linkedin',
        'stackoverflow',
        'startupjobs',
    ])


def run_spider(spider_name):
    return subprocess.run(['scrapy', 'crawl', spider_name], check=True)


if __name__ == '__main__':
    main()
