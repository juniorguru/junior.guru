import sys
from pathlib import Path

from peewee import Model, SqliteDatabase, CharField, IntegerField


db_file = Path(__file__).parent.parent / 'juniorguru' / 'data' / 'data.db'
db = SqliteDatabase(db_file)


class JobError(Model):
    class Meta:
        database = db

    message = CharField()
    source = CharField()


class SpiderMetric(Model):
    class Meta:
        database = db

    spider_name = CharField()
    name = CharField(index=True)
    value = IntegerField()


with db:
    job_errors = list(JobError.select())
    spider_errors = list(SpiderMetric.select().where(SpiderMetric.name == 'log_count/ERROR'))
if job_errors or spider_errors:
    print(f'Found {len(job_errors)} job errors.', file=sys.stderr)
    for job_error in job_errors:
        print(f'💥 {job_error.source}: {job_error.message}')
    print(f'Found {len(spider_errors)} spiders with uncaught errors.', file=sys.stderr)
    for spider_error in spider_errors:
        print(f'💥 {spider_error.spider_name}: {spider_error.name}={spider_error.value}')
    sys.exit(1)
print('OK', file=sys.stderr)
