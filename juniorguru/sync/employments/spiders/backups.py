import io
import tarfile
import shutil
from pathlib import Path
import sqlite3

import arrow
from scrapy.utils.project import data_path
from scrapy import Spider as BaseSpider, Request


class Spider(BaseSpider):
    name = 'backups'
    project_url = 'https://circleci.com/api/v1.1/project/github/honzajavorek/junior.guru'

    filename_backup = 'backup.tar.gz'
    filename_db = './juniorguru/data/data.db'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.data_dir = data_path('backups', createdir=True)

    def start_requests(self):
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

            item = dict(ci_build_num=build_num,
                        ci_build_url=ci_job['build_url'],
                        ci_build_date=arrow.get(stop_time).date())
            yield Request(f'{self.project_url}/{build_num}/artifacts',
                          callback=self.parse_artifacts,
                          cb_kwargs=dict(item=item))

    def parse_artifacts(self, response, item):
        backup_artifacts = [artifact for artifact in response.json()
                            if artifact.get('path') == self.filename_backup]
        if backup_artifacts:
            yield Request(backup_artifacts[0]['url'],
                          callback=self.parse_artifact,
                          cb_kwargs=dict(item=item))

    def parse_artifact(self, response, item):
        # didn't figure out how to do this in a memory-efficient way :(
        file = io.BytesIO(response.body)
        with tarfile.open(fileobj=file) as tar:
            try:
                db_file = tar.extractfile(self.filename_db)
            except KeyError:
                return
            db_path = Path(self.data_dir) / f"{item['ci_build_num']}.db"
            with db_path.open('wb') as f:
                shutil.copyfileobj(db_file, f)
        yield from self.parse_database(db_path, item)

    def parse_database(self, db_path, item):
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        try:
            cursor = connection.cursor()
            for row in cursor.execute('SELECT * FROM job'):
                yield dict(db_table='job', **item, **row)
            for row in cursor.execute('SELECT * FROM jobdropped'):
                yield dict(db_table='jobdropped', **item, **row)
        finally:
            connection.close()


def is_sync_ci_job(ci_job):
    return ci_job.get('workflows', {}).get('job_name', '') in ('sync', 'fetch')


def is_nightly_ci_job(ci_job):
    return ci_job.get('workflows', {}).get('workflow_name', '') == 'nightly'
