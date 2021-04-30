import math
from datetime import date, timedelta

from peewee import IntegerField, DateTimeField, ForeignKeyField, CharField, BooleanField

from juniorguru.models.base import BaseModel, JSONField


TOP_MEMBERS_PERCENT = 0.05
RECENT_PERIOD_DAYS = 30
IS_NEW_PERIOD_DAYS = 15

INTRO_CHANNEL = 788823881024405544  # ahoj
UPVOTES_EXCLUDE_CHANNELS = [
    INTRO_CHANNEL,
    788822884948770846,  # pravidla
    789046675247333397,  # oznámení
    797040163325870092,  # offtopic
    788822884948770847,  # moderátoři
    797107515186741248,  # roboti
]


class MessageAuthor(BaseModel):
    id = IntegerField(primary_key=True)
    is_bot = BooleanField(default=False)
    is_member = BooleanField(default=True)
    has_avatar = BooleanField(default=False)
    display_name = CharField()
    joined_at = DateTimeField(null=True)

    roles = JSONField(default=lambda: [])
    roles_add = JSONField(default=lambda: [])
    roles_remove = JSONField(default=lambda: [])

    messages_count = IntegerField(null=True)
    recent_messages_count = IntegerField(null=True)
    upvotes_count = IntegerField(null=True)
    recent_upvotes_count = IntegerField(null=True)
    has_intro = BooleanField(null=True)
    first_seen_at = DateTimeField(null=True)

    def calc_messages_count(self):
        self.messages_count = self.list_messages.count()

    def calc_recent_messages_count(self, today=None):
        self.recent_messages_count = self.list_recent_messages(today).count()

    def calc_upvotes_count(self):
        messages = self.list_messages \
            .where(Message.channel_id.not_in(UPVOTES_EXCLUDE_CHANNELS))
        self.upvotes_count = sum([message.upvotes for message in messages])

    def calc_recent_upvotes_count(self, today=None):
        messages = self.list_recent_messages(today) \
            .where(Message.channel_id.not_in(UPVOTES_EXCLUDE_CHANNELS))
        self.recent_upvotes_count = sum([message.upvotes for message in messages])

    def calc_has_intro(self):
        intro_messages_count = self.list_messages \
            .where(Message.channel_id == INTRO_CHANNEL) \
            .count()
        self.has_intro = bool(intro_messages_count)

    def calc_first_seen_at(self):
        first_message = self.list_messages \
            .order_by(Message.created_at) \
            .first()
        self.first_seen_at = first_message.created_at if first_message else self.joined_at

    def list_recent_messages(self, today=None):
        recent_period_start_at = (today or date.today()) - timedelta(days=RECENT_PERIOD_DAYS)
        return self.list_messages.where(Message.created_at >= recent_period_start_at)

    def is_new(self, today=None):
        return (self.first_seen_at + timedelta(days=IS_NEW_PERIOD_DAYS)).date() >= (today or date.today())

    @classmethod
    def count(cls):
        return cls.select().count()

    @classmethod
    def top_members_limit(cls):
        return math.ceil(cls.count() * TOP_MEMBERS_PERCENT)

    @classmethod
    def members_listing(cls):
        return cls.select().where(cls.is_bot == False, cls.is_member == True)


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

    @classmethod
    def channel_listing(cls, channel_id):
        return cls.select() \
            .where(cls.channel_id == channel_id) \
            .order_by(cls.created_at)
