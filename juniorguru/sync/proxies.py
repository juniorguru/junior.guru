import re
from pathlib import Path

import requests

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.sync.scrape_jobs.settings import PROXIES_FILE


logger = loggers.from_path(__file__)


@cli.sync_command()
def main():
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

    urls = [f'http://{line}' for line in text.splitlines()]
    logger.info(f'Got {len(urls)} proxies')

    proxies_list_path = Path(PROXIES_FILE)
    logger.info(f'Writing proxies to {proxies_list_path}')
    proxies_list_path.write_text('\n'.join(urls))
