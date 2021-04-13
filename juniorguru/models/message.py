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

    def messages_count(self):
        return self.list_messages.count()

    def messages_listing(self):
        return self.list_messages.order_by(Message.reactions_count.desc())

    def channels_listing(self):
        return sorted({message.channel_name for message in self.list_messages})
