import random
from functools import lru_cache
from multiprocessing import Pool

import requests
from lxml import html
from scrapy.downloadermiddlewares.retry import RetryMiddleware

from juniorguru.lib import loggers


logger = loggers.get('proxies')


class ScrapingProxyMiddleware():
    EXCEPTIONS_TO_RETRY = RetryMiddleware.EXCEPTIONS_TO_RETRY

    @classmethod
    def from_crawler(cls, crawler):
        proxies = scrape_proxies() if crawler.settings.PROXIES_ENABLED else []
        return cls(proxies, crawler.settings)

    def __init__(self, proxies, settings):
        self.proxies = proxies
        self.user_agents = settings.PROXIES_USER_AGENTS

    def get_proxy(self):
        return random.choice(self.proxies[:5]) if self.proxies else None

    def get_user_agent(self):
        return random.choice(self.user_agents)

    def rotate_user_agent(self, headers):
        headers = {n: v for n, v in headers.items() if n.lower() != 'user-agent'}
        return {'User-Agent': self.get_user_agent(), **headers}

    def rotate_proxies(self, request):
        logger.warning(f'Rotating proxies (currently {len(self.proxies)})')
        meta = {k: v for k, v in request.meta.items() if k != 'proxy'}
        try:
            self.proxies.remove(request.meta.get('proxy'))
        except ValueError:
            pass
        proxy = self.get_proxy()
        if proxy:
            return request.replace(headers=self.rotate_user_agent(request.headers),
                                   meta={'proxy': proxy, **meta},
                                   dont_filter=True)
        logger.warning('No proxies left, continuing without proxy')
        return request.replace(headers=self.rotate_user_agent(request.headers),
                               meta=meta,
                               dont_filter=True)

    def process_request(self, request, spider):
        if not getattr(spider, 'proxy', False):
            return
        user_agent = self.get_user_agent()
        request.headers['User-Agent'] = user_agent
        proxy = self.get_proxy()
        if proxy:
            logger.debug(f"Proxying {request!r} via {proxy} ({user_agent})")
            request.meta['proxy'] = proxy

    def process_exception(self, request, exception, spider):
        if not getattr(spider, 'proxy', False) or not request.meta.get('proxy'):
            return
        logger.debug(f'Got proxy exception {exception!r} for {request!r}')
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            return self.rotate_proxies(request)

    def process_response(self, request, response, spider):
        if not getattr(spider, 'proxy', False) or not request.meta.get('proxy'):
            return response
        if response.status in [504, 999] or 'mgts.ru' in response.url:
            user_agent = request.headers.get('User-Agent').decode()
            proxy = request.meta['proxy']
            logger.info(f"Got {response!r} proxied via {proxy} ({user_agent})")
            return self.rotate_proxies(request)
        logger.debug(f'Got proxied response {response!r}')
        return response


@lru_cache
def scrape_proxies():
    urls = []
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
            urls.append(f"http://{data['IP Address']}:{data['Port']}")
    random.shuffle(urls)
    logger.info(f'Scraped {len(urls)} proxies')

    speedy_urls = []
    pool = Pool(15)
    counter = 0
    for proxy in pool.imap(verify_proxy_speed, urls):
        logger.info(f"Proxy {proxy['url']} speed is {proxy['speed_sec']}")
        if proxy['speed_sec'] < 1000:
            speedy_urls.append(proxy['url'])
            counter += 1
        if counter >= 10:
            logger.info('Found enough fast proxies')
            break
    pool.terminate()
    pool.join()
    return speedy_urls


def verify_proxy_speed(url):
    try:
        response = requests.head('https://honzajavorek.cz/',
                                 timeout=10,
                                 proxies=dict(http=url, https=url))
        speed_sec = int(response.elapsed.total_seconds())
    except:
        speed_sec = 1000
    return dict(url=url, speed_sec=speed_sec)


if __name__ == '__main__':
    scrape_proxies()
