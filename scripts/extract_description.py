import sys
from pathlib import Path

from peewee import CharField, Model, SqliteDatabase
from playhouse.sqlite_ext import JSONField


try:
    id_arg = sys.argv[1]
except IndexError:
    print('No job ID specified!', file=sys.stderr)
    sys.exit(1)


db_file = Path(__file__).parent.parent / 'juniorguru' / 'data' / 'data.db'
db = SqliteDatabase(db_file)


class Job(Model):
    class Meta:
        database = db

    id = CharField(primary_key=True)
    response_backup_path = CharField(null=True)
    item = JSONField(null=True)


class JobDropped(Model):
    class Meta:
        database = db

    response_backup_path = CharField(null=True)
    item = JSONField(null=True)


with db:
    try:
        job = Job.get_by_id(id_arg)
        print(job.item['description_raw'])
    except Job.DoesNotExist:
        try:
            job = Job.select() \
                .where(Job.response_backup_path.contains(id_arg)) \
                .get()
            print(job.item['description_raw'])
        except Job.DoesNotExist:
            try:
                job_dropped = JobDropped.select() \
                    .where(JobDropped.response_backup_path.contains(id_arg)) \
                    .get()
                print(job_dropped.item['description_raw'])
            except JobDropped.DoesNotExist:
                print('Not found', file=sys.stderr)
                sys.exit(1)
