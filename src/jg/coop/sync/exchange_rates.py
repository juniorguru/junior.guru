from decimal import Decimal

import click
from pydantic import BaseModel

from jg.coop.cli.sync import main as cli
from jg.coop.lib import apify, loggers
from jg.coop.models.base import db
from jg.coop.models.exchange_rate import ExchangeRate


logger = loggers.from_path(__file__)


class ExchangeRateItem(BaseModel):
    code: str
    rate: Decimal


def parse_currencies(
    context: click.Context, param: click.Parameter, value: str
) -> set[str]:
    currencies = {currency.strip().upper() for currency in value.split(",")}
    currencies.discard("")
    if not currencies:
        raise click.BadParameter("Provide at least one currency code")
    return currencies


@cli.sync_command()
@click.option(
    "--currencies",
    default="EUR,USD",
    callback=parse_currencies,
    show_default=True,
)
@db.connection_context()
def main(currencies: set[str]):
    ExchangeRate.drop_table()
    ExchangeRate.create_table()

    for item in apify.fetch_data("honzajavorek/exchange-rates"):
        exchange_rate = ExchangeRateItem(**item)
        if exchange_rate.code not in currencies:
            continue
        logger.info(
            f"Saving exchange rate for {exchange_rate.code}: {exchange_rate.rate}"
        )
        ExchangeRate.create(**exchange_rate.model_dump())
