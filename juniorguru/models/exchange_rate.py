from decimal import Decimal

from peewee import CharField, DecimalField

from juniorguru.models.base import BaseModel


class ExchangeRate(BaseModel):
    code = CharField()
    rate = DecimalField()

    @classmethod
    def in_currency(cls, amount_czk: Decimal | int | float, currency: str) -> Decimal:
        return int(amount_czk / ExchangeRate.get(code=currency.upper()).rate)
