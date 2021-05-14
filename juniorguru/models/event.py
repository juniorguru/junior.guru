from peewee import CharField, DateTimeField, ForeignKeyField, TextField

from juniorguru.models.base import BaseModel, JSONField
from juniorguru.models import MessageAuthor


class Event(BaseModel):
    title = CharField()
    start_at = DateTimeField(index=True)
    description = TextField()
    poster_description = TextField(null=True)
    bio = TextField(null=True)
    bio_links = JSONField(default=lambda: [])
    recording_url = CharField(null=True)
    poster_path = CharField(null=True)
    logo_path = CharField(null=True)

    @classmethod
    def list_speaking_members(cls):
        return MessageAuthor.select() \
            .where(MessageAuthor.is_member == True) \
            .join(EventSpeaking)


class EventSpeaking(BaseModel):
    speaker = ForeignKeyField(MessageAuthor, backref='list_speaking')
    event = ForeignKeyField(Event, backref='list_speaking')
    avatar_path = CharField(null=True)
