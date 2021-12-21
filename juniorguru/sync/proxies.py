import os
from multiprocessing import Pool
import random

import requests
from lxml import html

from juniorguru.lib.timer import measure
from juniorguru.models import Proxy, with_db
from juniorguru.lib import loggers


PROXIES_ENABLED = bool(int(os.getenv('PROXIES_ENABLED', 0)))


logger = loggers.get('proxies')


@measure('proxies')
@with_db
def main():
    proxies = []
    if PROXIES_ENABLED:
        response = requests.get('https://free-proxy-list.net/', headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8,cs;q=0.6,sk;q=0.4,es;q=0.2',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:81.0) Gecko/20100101 Firefox/81.0',
            'Referer': 'https://www.sslproxies.org/',
        })
        response.raise_for_status()
        html_tree = html.fromstring(response.text)
        rows = iter(html_tree.cssselect('.table-striped tr'))
        headers = [col.text_content() for col in next(rows)]
        for row in rows:
            values = [(col.text_content() or '').strip() for col in row]
            data = dict(zip(headers, values))
            if data['IP Address'] and data['Port']:
                proxies.append(f"http://{data['IP Address']}:{data['Port']}")
        random.shuffle(proxies)

    Proxy.drop_table()
    Proxy.create_table()

    pool = Pool(15)
    counter = 0
    for record in pool.imap(test, proxies):
        if record['speed_sec'] < 1000:
            Proxy.create(**record)
            counter += 1
        if counter >= 10:
            logger.info('Found enough fast proxies, stopping!')
            break
    pool.terminate()
    pool.join()


def test(proxy):
    try:
        response = requests.head('https://honzajavorek.cz/',
                                 timeout=10,
                                 proxies=dict(http=proxy, https=proxy))
        speed_sec = int(response.elapsed.total_seconds())
    except:
        speed_sec = 1000
    logger.info(f"Proxy {proxy} speed is {speed_sec}")
    return dict(address=proxy, speed_sec=speed_sec)


if __name__ == '__main__':
    main()
