from peewee import CharField, IntegerField

from jg.coop.models.base import BaseModel, JSONField


class TopicMention(BaseModel):
    name = CharField(primary_key=True)
    mentions_count = IntegerField(default=0)
    mentions_last_month_count = IntegerField(default=0)


class TopicDiscussion(BaseModel):
    name = CharField(unique=True, null=True)
    channel_ids = JSONField(default=list)
    icon = CharField(null=True)
    monthly_letters_count = IntegerField(default=0)
    page_src_uris = JSONField(default=list)

    @property
    def is_hot(self) -> bool:
        return self.monthly_letters_count > 50000

    @classmethod
    def listing(cls):
        return (
            cls.select()
            .where(cls.name.is_null(False))
            .order_by(cls.monthly_letters_count.desc())
        )
