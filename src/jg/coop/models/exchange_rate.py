from decimal import Decimal

from peewee import CharField, DecimalField

from jg.coop.models.base import BaseModel


class ExchangeRate(BaseModel):
    code = CharField(unique=True)
    rate = DecimalField()

    @classmethod
    def in_currency(cls, amount_czk: Decimal | int | float, currency: str) -> Decimal:
        return int(amount_czk / ExchangeRate.get(code=currency.upper()).rate)

    @classmethod
    def from_currency(cls, amount: Decimal | int | float, currency: str) -> Decimal:
        return int(amount * ExchangeRate.get(code=currency.upper()).rate)
