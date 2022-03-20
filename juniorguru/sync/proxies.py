from pathlib import Path

import requests
from lxml import html

from juniorguru.lib.tasks import sync_task
from juniorguru.lib import loggers
from juniorguru.sync.scrape_jobs.settings import PROXIES_FILE


VERIFY_WORKERS = 15
VERIFY_TIMEOUT = 20
VERIFY_URL = 'https://www.linkedin.com'


logger = loggers.get(__name__)


@sync_task()
def main():
    logger.info('Scraping proxies')
    response = requests.get('https://free-proxy-list.net/', headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8,cs;q=0.6,sk;q=0.4,es;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Referer': 'https://www.sslproxies.org/',
    })
    response.raise_for_status()

    logger.info('Parsing proxies')
    html_tree = html.fromstring(response.text)
    rows = iter(html_tree.cssselect('.table-striped tr'))
    headers = [col.text_content() for col in next(rows)]
    urls = []
    for row in rows:
        values = [(col.text_content() or '').strip() for col in row]
        data = dict(zip(headers, values))
        if data['IP Address'] and data['Port']:
            urls.append(f"http://{data['IP Address']}:{data['Port']}")
    logger.info(f'Got {len(urls)} proxies')

    proxies_list_path = Path(PROXIES_FILE)
    logger.info(f'Writing proxies to {proxies_list_path}')
    proxies_list_path.write_text('\n'.join(urls))
