import datetime
import json
import os
import shutil
import subprocess
from multiprocessing import Pool
from operator import itemgetter
from pathlib import Path

from juniorguru.fetch.lib import timer
from juniorguru.fetch.lib.google import download_sheet
from juniorguru.fetch.lib.jobs_sheet import coerce_record
from juniorguru.models import Job, JobDropped, JobError, db


@timer.notify
def main():
    doc_key = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'
    records = download_sheet(doc_key, 'jobs')

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
