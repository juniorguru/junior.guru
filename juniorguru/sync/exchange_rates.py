from strictyaml import Map, Seq, Str

from juniorguru.cli.sync import main as cli
from juniorguru.lib import apify, loggers
from juniorguru.lib.yaml import Decimal as Dec
from juniorguru.models.base import db
from juniorguru.models.exchange_rate import ExchangeRate


logger = loggers.from_path(__file__)


CURRENCIES = ["EUR", "USD"]

YAML_SCHEMA = Seq(
    Map(
        {
            "code": Str(),
            "rate": Dec(),
        }
    )
)


@cli.sync_command()
@db.connection_context()
def main():
    ExchangeRate.drop_table()
    ExchangeRate.create_table()

    for exchange_rate in (
        item
        for item in apify.fetch_data("honzajavorek/exchange-rates")
        if item["code"] in CURRENCIES
    ):
        logger.info(
            f"Saving exchange rate for {exchange_rate['code']}: {exchange_rate['rate']}"
        )
        ExchangeRate.create(code=exchange_rate["code"], rate=exchange_rate["rate"])
