from datetime import date, timedelta
from decimal import Decimal
from typing import Tuple

import requests

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.models.base import db
from juniorguru.models.exchange_rate import ExchangeRate


logger = loggers.from_path(__file__)


CURRENCIES = ['EUR', 'USD']


@cli.sync_command()
@db.connection_context()
def main():
    monday = get_last_monday(date.today())
    logger.info(f'Getting exchange rates for {monday}')
    url = ('https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/'
           'denni_kurz.txt'
           f'?date={monday:%d.%m.%Y}')
    response = requests.get(url, headers={'User-Agent': 'JuniorGuruBot (+https://junior.guru)'})
    response.raise_for_status()

    exchange_rates = dict(parse_exchange_rate(line) for line in parse_lines(response.text))

    ExchangeRate.drop_table()
    ExchangeRate.create_table()

    for currency in CURRENCIES:
        logger.info(f'Saving exchange rate for {currency}: {exchange_rates[currency]}')
        ExchangeRate.create(code=currency, rate=exchange_rates[currency])


def get_last_monday(today) -> date:
    return today - timedelta(days=today.weekday())


def parse_exchange_rate(line) -> Tuple[str, Decimal]:
    code = line.split('|')[3]
    rate = Decimal(line.split('|')[4].replace(',', '.'))
    return code, rate


def parse_lines(text: str) -> list[str]:
    return text.strip().splitlines()[2:]
