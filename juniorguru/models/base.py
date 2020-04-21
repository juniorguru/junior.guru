from pathlib import Path

from peewee import SqliteDatabase, Model


db_file = Path(__file__).parent / '..' / 'data' / 'data.db'
db = SqliteDatabase(db_file, check_same_thread=False)


class BaseModel(Model):
    class Meta:
        database = db
