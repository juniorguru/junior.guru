import math
from datetime import date, timedelta
from itertools import groupby
from operator import attrgetter
from typing import Iterable, Self

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    TextField,
    fn,
)

from juniorguru.lib.coupons import parse_coupon
from juniorguru.lib.discord_club import ClubChannelID, ClubMemberID, parse_message_url
from juniorguru.models.base import BaseModel, JSONField


TOP_MEMBERS_PERCENT = 0.05

RECENT_PERIOD_DAYS = 30

YEAR_PERIOD_DAYS = 365

IS_NEW_PERIOD_DAYS = 15

UPVOTES_EXCLUDE_CHANNELS = [
    ClubChannelID.INTRO,
    ClubChannelID.ANNOUNCEMENTS,
    ClubChannelID.BOT,
    ClubChannelID.DASHBOARD,
    ClubChannelID.FUN,
    ClubChannelID.FUN_TOPICS,
]

STATS_EXCLUDE_CHANNELS = [
    ClubChannelID.ANNOUNCEMENTS,
    ClubChannelID.JOBS,
    ClubChannelID.BOT,
    ClubChannelID.DASHBOARD,
    ClubChannelID.FUN,
    ClubChannelID.FUN_TOPICS,
    834443926655598592,  # práce-bot (archived)
]


class ClubUser(BaseModel):
    id = IntegerField(primary_key=True)
    account_id = IntegerField(null=True, unique=True)
    subscription_id = CharField(null=True)
    joined_at = DateTimeField(null=True)
    subscribed_at = DateTimeField(null=True)
    subscribed_days = IntegerField(null=True)
    expires_at = DateTimeField(null=True)
    is_bot = BooleanField(default=False)
    is_member = BooleanField(default=True)
    has_avatar = BooleanField(default=True)
    avatar_path = CharField(null=True)
    display_name = CharField()
    has_feminine_name = BooleanField(null=True)
    mention = CharField(unique=True)
    coupon = CharField(null=True, index=True)
    initial_roles = JSONField(default=list)
    updated_roles = JSONField(null=True)
    dm_channel_id = IntegerField(null=True, unique=True)
    onboarding_channel_id = IntegerField(null=True, unique=True)
    total_spend = IntegerField(null=True)

    @property
    def joined_on(self):
        return self.joined_at.date() if self.joined_at else None

    @property
    def subscribed_on(self):
        return self.subscribed_at.date() if self.subscribed_at else None

    @property
    def intro(self):
        return self.list_public_messages \
            .where(ClubMessage.channel_id == ClubChannelID.INTRO,
                   ClubMessage.type == 'default') \
            .order_by(ClubMessage.created_at.desc()) \
            .first()

    @property
    def list_public_messages(self):
        return self.list_messages \
            .where(ClubMessage.is_private == False) \
            .order_by(ClubMessage.created_at.desc())

    @property
    def intro_thread_id(self):
        intro = self.intro
        return intro.id if intro else None

    def update_expires_at(self, expires_at):
        self.expires_at = non_empty_max([self.expires_at, expires_at])

    def content_size(self, private=False) -> int:
        list_messages = self.list_messages if private else self.list_public_messages
        return sum(message.content_size for message in list_messages)

    def recent_content_size(self, today=None, days=RECENT_PERIOD_DAYS, private=False) -> int:
        messages = self.list_recent_messages(today, days=days, private=private)
        return sum(message.content_size for message in messages)

    def messages_count(self, private=False):
        list_messages = self.list_messages if private else self.list_public_messages
        return list_messages.count()

    def upvotes_count(self, private=False):
        list_messages = self.list_messages if private else self.list_public_messages
        messages = list_messages \
            .where(ClubMessage.parent_channel_id.not_in(UPVOTES_EXCLUDE_CHANNELS))
        return sum([message.upvotes_count for message in messages])

    def recent_upvotes_count(self, today=None, private=False):
        messages = self.list_recent_messages(today, private=private) \
            .where(ClubMessage.parent_channel_id.not_in(UPVOTES_EXCLUDE_CHANNELS))
        return sum([message.upvotes_count for message in messages])

    def first_seen_on(self):
        first_message = self.list_messages \
            .order_by(ClubMessage.created_at) \
            .first()
        if not first_message:
            first_pin = self.list_pins \
                .join(ClubMessage, on=(ClubPin.pinned_message == ClubMessage.id)) \
                .order_by(ClubMessage.created_at) \
                .first()
            first_message = first_pin.pinned_message if first_pin else None
        return first_message.created_at.date() if first_message else self.joined_on

    def list_recent_messages(self, today=None, days=RECENT_PERIOD_DAYS, private=False):
        list_messages = self.list_messages if private else self.list_public_messages
        recent_period_start_at = (today or date.today()) - timedelta(days=days)
        return list_messages \
            .where(ClubMessage.created_at >= recent_period_start_at) \
            .order_by(ClubMessage.created_at.desc())

    def is_new(self, today=None):
        return (self.first_seen_on() + timedelta(days=IS_NEW_PERIOD_DAYS)) >= (today or date.today())

    @property
    def is_year_old(self) -> bool:
        if self.subscribed_days is None:
            # can happen for users like ClubMemberID.HONZA, ClubMemberID.HONZA_TEST
            return False
        return self.subscribed_days >= YEAR_PERIOD_DAYS

    def is_founder(self):
        return bool(self.coupon and parse_coupon(self.coupon)['slug'] in ('founders', 'founder'))

    @classmethod
    def get_member_by_id(cls, id):
        return cls.members_listing() \
            .where(cls.id == id) \
            .get()

    @classmethod
    def count(cls):
        return cls.listing().count()

    @classmethod
    def members_count(cls) -> int:
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
        members = cls.listing() \
            .where(cls.is_bot == False,
                   cls.is_member == True)
        if shuffle:
            members = members.order_by(fn.random())
        return members

    @classmethod
    def onboarding_listing(cls):
        return cls.members_listing().where(cls.onboarding_channel_id.is_null(False))

    @classmethod
    def avatars_listing(cls):
        return cls.members_listing().where(cls.avatar_path.is_null(False))

    @classmethod
    def core_discount_listing(cls, today: date = None, expiration_buffer_days: int = 10) -> Iterable[Self]:
        today = today or date.today()
        return cls.members_listing() \
            .where(cls.subscribed_days >= YEAR_PERIOD_DAYS,
                   cls.coupon.is_null(),
                   cls.expires_at >= today,
                   cls.expires_at <= today + timedelta(days=expiration_buffer_days))


class ClubMessage(BaseModel):
    id = IntegerField(primary_key=True)
    url = CharField()
    content = TextField()
    content_size = IntegerField()
    content_starting_emoji = CharField(null=True, index=True)
    reactions = JSONField(default=dict)
    upvotes_count = IntegerField(default=0)
    downvotes_count = IntegerField(default=0)
    created_at = DateTimeField(index=True)
    created_month = CharField(index=True)
    author = ForeignKeyField(ClubUser, backref='list_messages')
    author_is_bot = BooleanField()
    channel_id = IntegerField(index=True)
    channel_name = CharField()
    parent_channel_id = IntegerField(index=True)
    parent_channel_name = CharField()
    category_id = IntegerField(index=True, null=True)
    type = CharField(default='default')
    is_private = BooleanField(default=False)
    pinned_message_url = IntegerField(null=True, index=True)

    @property
    def is_pinning(self):
        return bool(self.pinned_message_url)

    @property
    def is_intro(self):
        return self.author.intro.id == self.id

    @property
    def dm_member(self):
        return ClubUser.get(dm_channel_id=self.channel_id)

    @property
    def pin(self):
        return self._pin.first()

    def record_pin(self):
        if not self.is_pinning:
            raise ValueError('Message is not a pinning message')
        pinned_message_id = parse_message_url(self.pinned_message_url)['message_id']
        rows_count = ClubPin \
            .update({ClubPin.pinning_message: self}) \
            .where(ClubPin.pinned_message == pinned_message_id,
                   ClubPin.member == self.dm_member) \
            .execute()
        if rows_count != 1:
            raise ClubPin.DoesNotExist()

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def content_size_by_month(cls, date):
        messages = cls.select() \
            .where(cls.created_month == f'{date:%Y-%m}') \
            .where(cls.author_is_bot == False) \
            .where(cls.is_private == False) \
            .where(cls.channel_id.not_in(STATS_EXCLUDE_CHANNELS))
        return sum(message.content_size for message in messages)

    @classmethod
    def listing(cls):
        return cls.select() \
            .where(cls.is_private == False) \
            .order_by(cls.created_at)

    @classmethod
    def pinning_listing(cls):
        return cls.select() \
            .where(cls.pinned_message_url.is_null(False)) \
            .order_by(cls.created_at)

    @classmethod
    def channel_listing(cls, channel_id):
        return cls.select() \
            .where(cls.channel_id == channel_id) \
            .order_by(cls.created_at)

    @classmethod
    def channel_listing_bot(cls, channel_id, starting_emoji=None):
        query = cls.channel_listing(channel_id) \
            .where(cls.author_is_bot == True)
        if starting_emoji:
            query = query.where(cls.content_starting_emoji == starting_emoji)
        return query

    @classmethod
    def channel_listing_since(cls, channel_id, since_at):
        return cls.select() \
            .where((cls.channel_id == channel_id)
                   & (cls.created_at >= since_at)) \
            .order_by(cls.created_at)

    @classmethod
    def digest_listing(cls, since_dt, limit=5):
        return cls.select() \
            .where(cls.is_private == False,
                   ClubMessage.parent_channel_id.not_in(UPVOTES_EXCLUDE_CHANNELS),
                   cls.created_at >= since_dt) \
            .order_by(cls.upvotes_count.desc()) \
            .limit(limit)

    @classmethod
    def digest_channels(cls, since_dt, limit=5):
        size = fn.sum(cls.content_size).alias('size')
        return cls.select(size,
                          cls.channel_id, cls.channel_name,
                          cls.parent_channel_id, cls.parent_channel_name) \
            .where(cls.is_private == False,
                   ClubMessage.parent_channel_id.not_in(UPVOTES_EXCLUDE_CHANNELS),
                   cls.created_at >= since_dt) \
            .group_by(cls.channel_id) \
            .order_by(size.desc()) \
            .limit(limit) \
            .dicts()

    @classmethod
    def last_message(cls, channel_id=None):
        query = cls.select()
        if channel_id is not None:
            query = query.where(cls.channel_id == channel_id)
        return query.order_by(cls.created_at.desc()).first()

    @classmethod
    def last_bot_message(cls, channel_id, starting_emoji=None, contains_text=None):
        query = cls.select() \
            .where(cls.author_is_bot == True,
                   cls.channel_id == channel_id) \
            .order_by(cls.created_at.desc())
        if starting_emoji:
            query = query.where(cls.content_starting_emoji == starting_emoji)
        if contains_text:
            query = query.where(cls.content.contains(contains_text))
        return query.first()


class ClubPin(BaseModel):
    pinned_message = ForeignKeyField(ClubMessage, backref='list_pins')
    member = ForeignKeyField(ClubUser, backref='list_pins')
    pinning_message = ForeignKeyField(ClubMessage, backref='_pin', null=True, unique=True)

    @classmethod
    def count(cls):
        return cls.select().count()

    @classmethod
    def outstanding_by_member(cls):
        pins = cls.select() \
            .join(ClubUser) \
            .where(cls.pinning_message.is_null(True),
                   ClubUser.dm_channel_id.is_null(False)) \
            .order_by(ClubUser.id)
        return groupby(pins, attrgetter('member'))

    @classmethod
    def honza_listing(cls):
        return cls.select() \
            .join(ClubUser) \
            .switch(cls) \
            .join(ClubMessage, on=(ClubPin.pinning_message_id == ClubMessage.id)) \
            .where(ClubUser.id == ClubMemberID.HONZA) \
            .order_by(ClubMessage.created_at)


class ClubDocumentedRole(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    mention = CharField(unique=True)
    slug = CharField(unique=True)
    description = TextField()
    position = IntegerField(unique=True)
    emoji = CharField(null=True)

    @classmethod
    def get_by_slug(cls, slug):
        if not slug:
            raise ValueError(repr(slug))
        return cls.select() \
            .where(cls.slug == slug) \
            .get()

    @classmethod
    def listing(cls):
        return cls.select() \
            .order_by(cls.position)


def non_empty_min(values):
    values = list(filter(None, values))
    if values:
        return min(values)
    return None


def non_empty_max(values):
    values = list(filter(None, values))
    if values:
        return max(values)
    return None
