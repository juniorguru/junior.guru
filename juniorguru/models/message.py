from peewee import CharField, IntegerField, TextField, ManyToManyField

from juniorguru.models.base import BaseModel


class Message(BaseModel):
    id = CharField(primary_key=True)
    channel_name = CharField()
    reactions_count = IntegerField()
    content = TextField()


class Keyword(BaseModel):
    name = CharField(primary_key=True)
    list_messages = ManyToManyField(Message, backref='list_keywords')

    @classmethod
    def messages_count(cls):
        return cls.list_messages().count()

    @classmethod
    def messages_listing(cls):
        return cls.list_messages().order_by(Message.reactions_count.desc())
