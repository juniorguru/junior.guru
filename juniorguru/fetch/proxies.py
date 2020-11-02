from multiprocessing import Pool

import requests
from lxml import html

from juniorguru.models import Proxy, db


def main():
    proxies = []
    response = requests.get('https://free-proxy-list.net/', headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8,cs;q=0.6,sk;q=0.4,es;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Referer': 'https://www.sslproxies.org/',
    })
    response.raise_for_status()
    html_tree = html.fromstring(response.text)
    rows = iter(html_tree.cssselect('#proxylisttable tr'))
    headers = [col.text_content() for col in next(rows)]
    for row in rows:
        values = [(col.text_content() or '').strip() for col in row]
        data = dict(zip(headers, values))
        proxies.append(f"http://{data['IP Address']}:{data['Port']}")
    records = Pool(15).map(test, proxies)

    with db:
        Proxy.drop_table()
        Proxy.create_table()

        for record in records:
            Proxy.create(**record)


def test(proxy):
    try:
        response = requests.head('https://httpbin.org/ip',
                                 timeout=10,
                                 proxies=dict(http=proxy, https=proxy))
        speed_sec = int(response.elapsed.total_seconds())
    except:
        speed_sec = 1000
    return dict(address=proxy, speed_sec=speed_sec)


if __name__ == '__main__':
    main()
