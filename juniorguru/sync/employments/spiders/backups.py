import io
import tarfile
import shutil
from pathlib import Path
import sqlite3
import json

import arrow
from scrapy.utils.project import data_path
from scrapy import Spider as BaseSpider, Request


class Spider(BaseSpider):
    name = 'backups'
    project_url = 'https://circleci.com/api/v1.1/project/github/honzajavorek/junior.guru'

    filename_backup = 'backup.tar.gz'
    filename_db = './juniorguru/data/data.db'

    tables = [
        # old-style jobs tables
        'job',
        'jobdropped',

        # new-style jobs tables
        'employment',
        'employmentposting',
    ]

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.data_dir = data_path('backups', createdir=True)

    def start_requests(self):
        # probes just 10 pages as there are only last 30 backups anyway
        # https://circleci.com/docs/2.0/artifacts/
        limit = 100
        for offset in range(0, limit * 10, limit):
            yield Request(f'{self.project_url}?limit={limit}&offset={offset}')

    def parse(self, response):
        for ci_job in response.json():
            if not is_sync_ci_job(ci_job) or not is_nightly_ci_job(ci_job):
                continue

            build_num = ci_job.get('build_num')
            if not build_num:
                continue

            stop_time = ci_job.get('stop_time')
            if not stop_time:
                continue

            ci_data = dict(build_num=build_num,
                           build_url=ci_job['build_url'],
                           build_date=arrow.get(stop_time).date())
            yield Request(f'{self.project_url}/{build_num}/artifacts',
                          callback=self.parse_artifacts,
                          cb_kwargs=dict(ci_data=ci_data))

    def parse_artifacts(self, response, ci_data):
        backup_artifacts = [artifact for artifact in response.json()
                            if artifact.get('path') == self.filename_backup]
        if backup_artifacts:
            yield Request(backup_artifacts[0]['url'],
                          callback=self.parse_artifact,
                          cb_kwargs=dict(ci_data=ci_data))

    def parse_artifact(self, response, ci_data):
        # couldn't figure out how to do the following line in a memory-efficient way :(
        file = io.BytesIO(response.body)
        with tarfile.open(fileobj=file) as tar:
            try:
                db_file = tar.extractfile(self.filename_db)
            except KeyError:
                return
            db_path = Path(self.data_dir) / f"{ci_data['build_num']}.db"
            with db_path.open('wb') as f:
                shutil.copyfileobj(db_file, f)
        yield from self.parse_database(db_path, ci_data)

    def parse_database(self, db_path, ci_data):
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        try:
            cursor = connection.cursor()
            sql = f"SELECT name FROM sqlite_master WHERE name IN ({', '.join(['?' for _ in self.tables])})"
            tables = [row['name'] for row in cursor.execute(sql, self.tables)]
            for table in tables:
                for row in cursor.execute(f'SELECT * FROM {table}'):
                    yield from getattr(self, f'parse_{table}_row')(row, ci_data)
        finally:
            connection.close()

    def parse_job_row(self, row, ci_data):
        yield dict(title=row['title'],
                   url=row['link'],
                   company_name=row['company_name'],
                   description_html=row['description_html'],
                   seen_at=ci_data['build_date'],
                   source=row['source'],
                   source_url=row['response_url'],
                   backup_url=ci_data['build_url'])

    def parse_jobdropped_row(self, row, ci_data):
        if row['type'] == 'NotEntryLevel':
            item = json.loads(row['item'])
            yield dict(title=item['title'],
                       url=item['link'],
                       company_name=item['company_name'],
                       description_html=item['description_html'],
                       seen_at=ci_data['build_date'],
                       source=row['source'],
                       source_url=row['response_url'],
                       backup_url=ci_data['build_url'])

    def parse_employment_row(self, row, ci_data):
        raise NotImplementedError

    def parse_employmentposting_row(self, row, ci_data):
        raise NotImplementedError


def is_sync_ci_job(ci_job):
    return ci_job.get('workflows', {}).get('job_name', '') in ('sync', 'fetch')


def is_nightly_ci_job(ci_job):
    return ci_job.get('workflows', {}).get('workflow_name', '') == 'nightly'
