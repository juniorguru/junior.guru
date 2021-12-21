from peewee import CharField, DateField, IntegerField

from juniorguru.models.base import BaseModel


class Transaction(BaseModel):
    happened_on = DateField(index=True)
    category = CharField()
    amount = IntegerField()
