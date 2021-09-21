import io
import tarfile
import shutil
from pathlib import Path
import sqlite3
import json
from datetime import date

import arrow
from scrapy.utils.project import data_path
from scrapy import Spider as BaseSpider, Request

from juniorguru.sync.employments.items import Employment


def employment_adapter(ci_data):
    for row in (yield 'SELECT * from employment'):
        for seen_at in (date.fromisoformat(row['first_seen_at']), date.fromisoformat(row['last_seen_at'])):
            yield Employment(title=row['title'],
                             urls=json.loads(row['urls']),
                             company_name=row['company_name'],
                             locations=row['locations'],
                             description_html=row['description_html'],
                             lang=row['lang'],
                             seen_at=seen_at,
                             source=row['source'],
                             source_urls=json.loads(row['source_urls']),
                             adapter='employment',
                             build_url=ci_data['build_url'])


def job_adapter(ci_data):  # old-style jobs
    for row in (yield 'SELECT * from job'):
        urls = [row['link']]
        urls += json.loads(row['alternative_links']) if 'alternative_links' in row else []

        for seen_at in (date.fromisoformat(row['posted_at']), ci_data['build_date']):
            yield Employment(title=row['title'],
                             urls=urls,
                             company_name=row['company_name'],
                             locations=json.loads(row['locations']),
                             description_html=row['description_html'],
                             lang=row['lang'],
                             seen_at=seen_at,
                             source=row['source'],
                             source_urls=[row['response_url']],
                             adapter='job',
                             build_url=ci_data['build_url'])


def jobdropped_adapter(ci_data):  # old-style jobs
    for row in (yield 'SELECT * from jobdropped WHERE type IN ("NotEntryLevel", "Expired")'):
        item = json.loads(row['item'])
        urls = [item['link']] + item.get('alternative_links', [])

        for seen_at in (date.fromisoformat(item['posted_at']), ci_data['build_date']):
            yield Employment(title=item['title'],
                             urls=urls,
                             company_name=item['company_name'],
                             locations=item.get('locations'),
                             description_html=item['description_html'],
                             lang=item.get('lang'),
                             seen_at=seen_at,
                             source=row['source'],
                             source_urls=[row['response_url']],
                             adapter='jobdropped',
                             build_url=ci_data['build_url'])


class Spider(BaseSpider):
    name = 'backups'
    custom_settings = {'ROBOTSTXT_OBEY': False}  # requesting API, so irrelevant, saving a few requests

    project_url = 'https://circleci.com/api/v1.1/project/github/honzajavorek/junior.guru'
    filename_backup = 'backup.tar.gz'
    filename_db = './juniorguru/data/data.db'
    adapters = [employment_adapter, job_adapter, jobdropped_adapter]

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
            for adapter_fn in self.adapters:
                yield from self.parse_rows(cursor, adapter_fn, ci_data)
        finally:
            connection.close()

    def parse_rows(self, cursor, adapter_fn, ci_data):
        adapter_gen = adapter_fn(ci_data)
        sql = next(adapter_gen)
        try:
            rows = cursor.execute(sql)
        except sqlite3.OperationalError as e:
            if 'no such table:' not in str(e):
                raise e
        else:
            adapter_gen.send(rows)
            yield from adapter_gen


def is_sync_ci_job(ci_job):
    return ci_job.get('workflows', {}).get('job_name', '') in ('sync', 'fetch')


def is_nightly_ci_job(ci_job):
    return ci_job.get('workflows', {}).get('workflow_name', '') == 'nightly'
