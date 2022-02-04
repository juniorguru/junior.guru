import re
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
from scrapy.exceptions import CloseSpider

from juniorguru.lib.url_params import strip_utm_params
from juniorguru.lib import loggers
from juniorguru.jobs.employments.items import EmploymentItem
from juniorguru.jobs.legacy_jobs.spiders.linkedin import clean_validated_url
from juniorguru.models import db, Employment


logger = loggers.get(__name__)


STARTUPJOBS_URL_RE = re.compile(r'startupjobs.+\&utm_')


def employment_v1_adapter(ci_data):
    for row in (yield 'SELECT * from employment_v1'):
        yield EmploymentItem(title=row['title'],
                             company_name=row['company_name'],
                             url=clean_validated_url(row['url']),
                             apply_url=clean_validated_url(row.get('apply_url')),
                             external_ids=json.loads(row['external_ids']),
                             locations=json.loads(row.get('locations', 'null')),
                             remote=row['remote'],
                             lang=row.get('lang'),
                             description_html=row['description_html'],
                             first_seen_at=date.fromisoformat(row['first_seen_at']),
                             last_seen_at=date.fromisoformat(row['last_seen_at']),
                             employment_types=json.loads(row.get('employment_types', 'null')),
                             juniority_re_score=row.get('juniority_re_score'),
                             juniority_ai_opinion=row.get('juniority_ai_opinion'),
                             juniority_votes_score=row['juniority_votes_score'],
                             juniority_votes_count=row['juniority_votes_count'],
                             source=row['source'],
                             source_urls=json.loads(row['source_urls']),
                             adapter='employment_v1',
                             build_url=ci_data['build_url'])


def job_adapter(ci_data):  # old-style jobs
    for row in (yield 'SELECT * from job'):
        apply_url = (row.get('apply_link') or
                     row.get('external_link') or
                     (row['link'] if ('link' in row and STARTUPJOBS_URL_RE.search(row['link'])) else None))

        if 'upvotes_count' in row and 'downvotes_count' in row:
            votes_score = row['upvotes_count'] - row['downvotes_count']
            votes_count = row['upvotes_count'] + row['downvotes_count']
        else:
            votes_score = 0
            votes_count = 0

        yield EmploymentItem(title=row['title'],
                             url=strip_utm_params(clean_validated_url(row['link'])),
                             apply_url=clean_validated_url(apply_url),
                             company_name=row['company_name'],
                             locations=json.loads(row['locations']),
                             remote=bool(row['remote']),
                             description_html=row['description_html'],
                             lang=row['lang'],
                             first_seen_at=date.fromisoformat(row['posted_at']),
                             last_seen_at=ci_data['build_date'],
                             juniority_re_score=row['junior_rank'],
                             juniority_ai_opinion=row.get('magic_is_junior'),
                             juniority_votes_score=votes_score,
                             juniority_votes_count=votes_count,
                             employment_types=json.loads(row['employment_types']),
                             source=row['source'],
                             source_urls=[row['response_url']],
                             adapter='job',
                             build_url=ci_data['build_url'])


def jobdropped_adapter(ci_data):  # old-style jobs
    for row in (yield 'SELECT * from jobdropped WHERE type IN ("NotEntryLevel", "Expired")'):
        item = json.loads(row['item'])

        first_seen_at = date.fromisoformat(item['posted_at'])
        if item.get('expires_at'):
            last_seen_at = min(ci_data['build_date'], date.fromisoformat(item['expires_at']))
        else:
            last_seen_at = ci_data['build_date']

        if 'upvotes_count' in row and 'downvotes_count' in row:
            votes_score = row['upvotes_count'] - row['downvotes_count']
            votes_count = row['upvotes_count'] + row['downvotes_count']
        else:
            votes_score = 0
            votes_count = 0

        yield EmploymentItem(title=item['title'],
                             url=strip_utm_params(clean_validated_url(item['link'])),
                             apply_url=clean_validated_url(item.get('apply_link')),
                             company_name=item['company_name'],
                             locations=item.get('locations'),
                             remote=item.get('remote', False),
                             description_html=item['description_html'],
                             lang=item.get('lang'),
                             first_seen_at=first_seen_at,
                             last_seen_at=last_seen_at,
                             juniority_re_score=item.get('junior_rank'),
                             juniority_ai_opinion=row.get('magic_is_junior'),
                             juniority_votes_score=votes_score,
                             juniority_votes_count=votes_count,
                             employment_types=item.get('employment_types'),
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
    adapters = [
        employment_v1_adapter,
        job_adapter,
        jobdropped_adapter,
    ]

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.data_dir = data_path('backups', createdir=True)
        self.saved_count = 0

    def start_requests(self):
        # https://circleci.com/docs/2.0/artifacts/
        limit = 100
        pages = 5
        for offset in range(0, limit * pages, limit):
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
        logger.info(f'Processing artifact {response.url} from build {repr(ci_data)}')

        # done with requests at this point, the following code blocks the async loop to process
        # the backups, so checking the number of employments loaded from backups and if it didn't
        # change from the last time, further processing is redundant
        with db:
            saved_count = Employment.loaded_from_backups_count()
        logger.info(f'Employments loaded from backups: {saved_count} (previously {self.saved_count})')
        if saved_count and saved_count == self.saved_count:
            raise CloseSpider('Everything loaded, no need to process more backups')
        else:
            self.saved_count = saved_count

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
        connection.row_factory = Row
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


class Row(sqlite3.Row):
    def get(self, key, default=None):
        return self[key] if key in self else default


def is_sync_ci_job(ci_job):
    return ci_job.get('workflows', {}).get('job_name', '') in ('sync', 'fetch')


def is_nightly_ci_job(ci_job):
    return ci_job.get('workflows', {}).get('workflow_name', '') == 'nightly'
