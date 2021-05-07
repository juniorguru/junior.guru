from peewee import CharField, DateTimeField, ForeignKeyField

from juniorguru.models.base import BaseModel
from juniorguru.models import MessageAuthor


class Event(BaseModel):
    title = CharField()
    start_at = DateTimeField(index=True)

    @classmethod
    def list_speaking_members(cls):
        return MessageAuthor.select() \
            .where(MessageAuthor.is_member == True) \
            .join(EventSpeaking)


class EventSpeaking(BaseModel):
    speaker = ForeignKeyField(MessageAuthor, backref='list_speaking')
    event = ForeignKeyField(Event, backref='list_speaking')
