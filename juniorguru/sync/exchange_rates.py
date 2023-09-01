from datetime import date, timedelta
from decimal import Decimal
from operator import itemgetter
from pathlib import Path
from typing import Tuple
import click

import strictyaml
from strictyaml import Seq, Map, Str
import requests

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.yaml import Decimal as Dec
from juniorguru.models.base import db
from juniorguru.models.exchange_rate import ExchangeRate


logger = loggers.from_path(__file__)


CURRENCIES = ['EUR', 'USD']

YAML_SCHEMA = Seq(
    Map({
        'code': Str(),
        'rate': Dec(),
    })
)


@cli.sync_command()
@click.option('--path', 'yaml_path', default='juniorguru/data/exhange_rates.yml', type=click.Path(path_type=Path))
@db.connection_context()
def main(yaml_path: Path):
    monday = get_last_monday(date.today())
    logger.info(f'Getting exchange rates for {monday}')
    try:
        url = ('https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/'
            'denni_kurz.txt'
            f'?date={monday:%d.%m.%Y}')
        response = requests.get(url, headers={'User-Agent': 'JuniorGuruBot (+https://junior.guru)'})
        response.raise_for_status()
    except requests.ConnectionError:
        logger.error('ČNB API is down, loading from YAML')
        exchange_rates = strictyaml.load(yaml_path.read_text(), YAML_SCHEMA).data
    else:
        exchange_rates = [parse_exchange_rate(line) for line in parse_lines(response.text)]
        exchange_rates = [exchange_rate for exchange_rate in exchange_rates if exchange_rate['code'] in CURRENCIES]
        exchange_rates = sorted(exchange_rates, key=itemgetter('code'))
        yaml_path.write_text(strictyaml.as_document(exchange_rates, YAML_SCHEMA).as_yaml())

    ExchangeRate.drop_table()
    ExchangeRate.create_table()

    for exchange_rate in exchange_rates:
        logger.info(f"Saving exchange rate for {exchange_rate['code']}: {exchange_rate['rate']}")
        ExchangeRate.create(code=exchange_rate['code'], rate=exchange_rate['rate'])


def get_last_monday(today) -> date:
    return today - timedelta(days=today.weekday())


def parse_exchange_rate(line) -> Tuple[str, str]:
    return dict(code=line.split('|')[3],
                rate=Decimal(line.split('|')[4].replace(',', '.')))


def parse_lines(text: str) -> list[str]:
    return text.strip().splitlines()[2:]
