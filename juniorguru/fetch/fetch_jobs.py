import os
import json
import shutil
import datetime
import subprocess
from multiprocessing import Pool
from pathlib import Path
from operator import itemgetter

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from .sheets import coerce_record
from ..models import db, Job
from ..scrapers.settings import MONITORING_EXPORT_DIR


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

    shutil.rmtree(MONITORING_EXPORT_DIR, ignore_errors=True)
    Pool(1).map(run_spider, [
        'stackoverflow',
        'startupjobs',
    ])


def run_spider(spider_name):
    return subprocess.run(['scrapy', 'crawl', spider_name], check=True)


if __name__ == '__main__':
    main()
