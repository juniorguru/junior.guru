from datetime import date, timedelta

from peewee import IntegerField, DateTimeField, ForeignKeyField, CharField, BooleanField

from juniorguru.models.base import BaseModel, JSONField


RECENT_DAYS_PERIOD = 30


class MessageAuthor(BaseModel):
    id = IntegerField(primary_key=True)
    is_bot = BooleanField(default=False)
    is_member = BooleanField(default=True)
    display_name = CharField()
    roles = JSONField(default=lambda: [])
    messages_count = IntegerField(null=True)
    recent_messages_count = IntegerField(null=True)

    def calc_messages_count(self):
        if self.messages_count is None:
            self.messages_count = self.list_messages.count()
        return self.messages_count

    def calc_recent_messages_count(self, today=None):
        if self.recent_messages_count is None:
            recent_period_start_at = (today or date.today()) - timedelta(days=RECENT_DAYS_PERIOD)
            self.recent_messages_count = self.list_messages \
                .where(Message.created_at >= recent_period_start_at).count()
        return self.recent_messages_count

    @classmethod
    def count(cls):
        return cls.select().count()

    @classmethod
    def members_listing(cls):
        return cls.select().where(cls.is_bot == False, cls.is_member == True)

    @classmethod
    def members_role_listing(cls, role_id):
        roles = cls.roles.children().alias('roles')
        return cls.members_listing() \
            .from_(cls, roles) \
            .where(roles.c.value == role_id)


class Message(BaseModel):
    id = IntegerField(primary_key=True)
    content = CharField()
    upvotes = IntegerField(default=0)
    downvotes = IntegerField(default=0)
    created_at = DateTimeField(index=True)
    author = ForeignKeyField(MessageAuthor, backref='list_messages')
    channel_id = IntegerField()
    channel_name = CharField()

    @classmethod
    def count(cls):
        return cls.select().count()

    @classmethod
    def history_listing(cls):
        return cls.select().order_by(cls.created_at)
