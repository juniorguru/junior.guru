import re

import requests

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.models.proxy import Proxy
from juniorguru.models.base import db


logger = loggers.from_path(__file__)


@cli.sync_command()
@db.connection_context()
def main():
    Proxy.drop_table()
    Proxy.create_table()

    # docs at https://docs.proxyscrape.com/
    logger.info('Scraping proxies')
    response = requests.get('https://api.proxyscrape.com/v2/',
                            params=dict(request='displayproxies',
                                        protocol='http',
                                        timeout=2000))
    response.raise_for_status()
    text = response.text
    if not re.search(r'^[\d\.\:\s]+$', text):
        raise Exception(f'{response.url} returned: {text}')

    for line in text.splitlines():
        Proxy.create(url=f'http://{line}')
    logger.info(f'Saved {len(Proxy.listing())} proxies')
