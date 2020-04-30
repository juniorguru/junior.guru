import sys
from pathlib import Path

from peewee import SqliteDatabase, Model


db_file = Path(__file__).parent.parent / 'juniorguru' / 'data' / 'data.db'
db = SqliteDatabase(db_file)


class JobError(Model):
    class Meta:
        database = db


with db:
    errors_count = JobError.select().count()
if errors_count:
    print(f'Found {errors_count} errors!', file=sys.stderr)
    sys.exit(1)
print('OK', file=sys.stderr)
