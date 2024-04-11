from peewee import CharField, TextField

from project.models.base import BaseModel


class Tip(BaseModel):
    slug = CharField(primary_key=True)
    emoji = CharField(unique=True)
    title = CharField()
    edit_url = CharField()
    club_url = CharField()
    lead = TextField()
    content = TextField()
