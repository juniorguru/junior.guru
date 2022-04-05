import math
from datetime import date, timedelta

from peewee import IntegerField, DateTimeField, ForeignKeyField, CharField, BooleanField, DateField, fn

from juniorguru.models.base import BaseModel, JSONField
from juniorguru.lib.club import (parse_coupon, INTRO_CHANNEL, UPVOTES_EXCLUDE_CHANNELS,
                                 CLUB_LAUNCH_ON, JUNIORGURU_BOT, TOP_MEMBERS_PERCENT,
                                 RECENT_PERIOD_DAYS, IS_NEW_PERIOD_DAYS)


class ClubUser(BaseModel):
    id = IntegerField(primary_key=True)
    subscription_id = CharField(null=True)
    is_bot = BooleanField(default=False)
    is_member = BooleanField(default=True)
    avatar_path = CharField(null=True)
    display_name = CharField()
    mention = CharField()
    coupon_base = CharField(null=True, index=True)
    joined_at = DateTimeField(null=True)
    expires_at = DateTimeField(null=True)
    roles = JSONField(default=lambda: [])
    sdacademy_student_started_on = DateField(null=True)

    def messages_count(self):
        return self.list_messages.count()

    def recent_messages_count(self, today=None):
        return self.list_recent_messages(today).count()

    def upvotes_count(self):
        messages = self.list_messages \
            .where(ClubMessage.channel_id.not_in(UPVOTES_EXCLUDE_CHANNELS))
        return sum([message.upvotes_count for message in messages])

    def recent_upvotes_count(self, today=None):
        messages = self.list_recent_messages(today) \
            .where(ClubMessage.channel_id.not_in(UPVOTES_EXCLUDE_CHANNELS))
        return sum([message.upvotes_count for message in messages])

    def has_intro(self, intro_channel_id=None):
        intro_channel_id = intro_channel_id or INTRO_CHANNEL
        intro_message = self.list_messages \
            .where(ClubMessage.channel_id == intro_channel_id, ClubMessage.type == 'default') \
            .first()
        return bool(intro_message)

    def first_seen_on(self):
        first_message = self.list_messages \
            .order_by(ClubMessage.created_at) \
            .first()
        if not first_message:
            first_pin = self.list_pins \
                .join(ClubMessage) \
                .order_by(ClubMessage.created_at) \
                .first()
            first_message = first_pin.message if first_pin else None
        return first_message.created_at.date() if first_message else self.joined_at.date()

    def list_recent_messages(self, today=None):
        recent_period_start_at = (today or date.today()) - timedelta(days=RECENT_PERIOD_DAYS)
        return self.list_messages.where(ClubMessage.created_at >= recent_period_start_at)

    def is_new(self, today=None):
        return (self.first_seen_on() + timedelta(days=IS_NEW_PERIOD_DAYS)) >= (today or date.today())

    def is_year_old(self, today=None):
        first_seen_on = min(self.joined_at.date(), self.first_seen_on())
        return first_seen_on.replace(year=first_seen_on.year + 1) <= (today or date.today())

    def is_founder(self):
        if self.coupon_base and parse_coupon(self.coupon_base)['coupon_name'] == 'FOUNDERS':
            return True
        joined_date = min(self.joined_at.date(), self.first_seen_on())
        if joined_date < CLUB_LAUNCH_ON:
            return True
        return False

    @classmethod
    def members_count(cls):
        return cls.members_listing().count()

    @classmethod
    def avatars_count(cls):
        return cls.avatars_listing().count()

    @classmethod
    def top_members_limit(cls):
        return math.ceil(cls.members_count() * TOP_MEMBERS_PERCENT)

    @classmethod
    def listing(cls):
        return cls.select()

    @classmethod
    def members_listing(cls, shuffle=False):
        members = cls.listing().where(cls.is_bot == False, cls.is_member == True)
        if shuffle:
            members = members.order_by(fn.random())
        return members

    @classmethod
    def avatars_listing(cls):
        return cls.members_listing().where(cls.avatar_path.is_null(False))


class ClubMessage(BaseModel):
    id = IntegerField(primary_key=True)
    url = CharField()
    content = CharField()
    upvotes_count = IntegerField(default=0)
    downvotes_count = IntegerField(default=0)
    pin_reactions_count = IntegerField(default=0)
    created_at = DateTimeField(index=True)
    author = ForeignKeyField(ClubUser, backref='list_messages')
    channel_id = IntegerField()
    channel_name = CharField()
    channel_mention = CharField()
    type = CharField(default='default')
    is_pinned = BooleanField(default=False)

    @classmethod
    def count(cls):
        return cls.select().count()

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.created_at)

    @classmethod
    def channel_listing(cls, channel_id):
        return cls.select() \
            .where(cls.channel_id == channel_id) \
            .order_by(cls.created_at)

    @classmethod
    def channel_listing_since(cls, channel_id, since_at):
        return cls.select() \
            .where((cls.channel_id == channel_id)
                   & (cls.created_at >= since_at)) \
            .order_by(cls.created_at)

    @classmethod
    def digest_listing(cls, since_dt, limit=5):
        return cls.select() \
            .where(cls.created_at >= since_dt,
                   ClubMessage.channel_id.not_in(UPVOTES_EXCLUDE_CHANNELS)) \
            .order_by(cls.upvotes_count.desc()) \
            .limit(limit)

    @classmethod
    def pinned_by_reactions_listing(cls, min_pins=1):
        return cls.select() \
            .where(cls.pin_reactions_count >= min_pins) \
            .order_by(cls.created_at)

    @classmethod
    def last_bot_message(cls, channel_id, startswith_emoji, contains_text=None):
        query = cls.select() \
            .join(ClubUser) \
            .where(ClubUser.id == JUNIORGURU_BOT,
                   cls.channel_id == channel_id,
                   cls.content.startswith(startswith_emoji)) \
            .order_by(cls.created_at.desc())
        if contains_text:
            query = query.where(cls.content.contains(contains_text))
        return query.first()


class ClubPinReaction(BaseModel):
    user = ForeignKeyField(ClubUser, backref='list_pins')
    message = ForeignKeyField(ClubMessage, backref='list_pins')

    @classmethod
    def count(cls):
        return cls.select().count()

    @classmethod
    def listing(cls):
        return cls.select()
