from pathlib import Path
import random
from multiprocessing import Pool

import requests
from scrapy.downloadermiddlewares.retry import RetryMiddleware

from juniorguru.lib import loggers


VERIFY_SPEED_WORKERS = 8

VERIFY_SPEED_TIMEOUT_SEC = 5

SCRAPING_BATCH_SIZE = 5

PROXIES_PATH = Path(__file__).parent.parent / 'data' / 'proxies.txt'


logger = loggers.get(__name__)


class ScrapingProxyMiddleware():
    EXCEPTIONS_TO_RETRY = RetryMiddleware.EXCEPTIONS_TO_RETRY

    DEFAULT_PROXIES_USER_AGENTS = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:75.0) Gecko/20100101 Firefox/75.0',
        'Mozilla/5.0 (iPhone; CPU OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/29.0 Mobile/15E148 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    ]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(enabled=crawler.settings.getbool('PROXIES_ENABLED'),
                   user_agents=crawler.settings.getlist('PROXIES_USER_AGENTS'))

    def __init__(self, enabled=False, user_agents=None):
        self.enabled = enabled
        self.user_agents = user_agents or self.DEFAULT_PROXIES_USER_AGENTS
        self.proxies = None
        self.proxies_batch = []

    def get_proxy(self):
        if self.proxies is None:
            self.proxies = generate_proxies()
        if not self.proxies_batch:
            self.proxies_batch = next(self.proxies)
        return random.choice(self.proxies_batch)

    def get_user_agent(self):
        return random.choice(self.user_agents)

    def rotate_user_agent(self, headers):
        headers = {n: v for n, v in headers.items() if n.lower() != 'user-agent'}
        return {'User-Agent': self.get_user_agent(), **headers}

    def rotate_proxies(self, request):
        logger.warning(f'Rotating proxies (currently {len(self.proxies_batch)})')
        meta = {k: v for k, v in request.meta.items() if k != 'proxy'}
        try:
            self.proxies_batch.remove(request.meta.get('proxy'))
        except ValueError:
            pass
        proxy = self.get_proxy()
        if proxy:
            return request.replace(headers=self.rotate_user_agent(request.headers),
                                   meta={'proxy': proxy, **meta},
                                   dont_filter=True)
        logger.warning('No proxies, continuing without proxy')
        return request.replace(headers=self.rotate_user_agent(request.headers),
                               meta=meta,
                               dont_filter=True)

    def process_request(self, request, spider):
        if not self.enabled or not getattr(spider, 'proxies', False):
            return
        if not request.meta.get('proxies', True):  # allows to explicitly turn proxies off for a particular request
            return
        user_agent = self.get_user_agent()
        request.headers['User-Agent'] = user_agent
        proxy = self.get_proxy()
        if proxy:
            logger.debug(f"Proxying {request!r} via {proxy} ({user_agent})")
            request.meta['proxy'] = proxy

    def process_exception(self, request, exception, spider):
        if not self.enabled or not getattr(spider, 'proxies', False):
            return
        if not request.meta.get('proxy'):  # proxies haven't been used for this request
            return
        logger.debug(f'Got proxy exception {exception!r} for {request!r}')
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            return self.rotate_proxies(request)

    def process_response(self, request, response, spider):
        if not self.enabled or not getattr(spider, 'proxies', False):
            return response
        if not request.meta.get('proxy'):  # proxies haven't been used for this request
            return
        if response.status in [504, 999] or 'mgts.ru' in response.url:
            user_agent = request.headers.get('User-Agent').decode()
            proxy = request.meta['proxy']
            logger.info(f"Got {response!r} proxied via {proxy} ({user_agent})")
            return self.rotate_proxies(request)
        logger.debug(f'Got proxied response {response!r}')
        return response


def generate_proxies():
    urls = PROXIES_PATH.read_text().splitlines()
    logger.info(f'Found {len(urls)} proxies')
    while True:
        random.shuffle(urls)
        speedy_urls = []
        with Pool(VERIFY_SPEED_WORKERS) as pool:
            counter = 0
            for proxy in pool.imap_unordered(verify_proxy_speed, urls):
                if proxy['speed_sec'] < 1000:
                    logger.info(f"Proxy {proxy['url']} speed is {proxy['speed_sec']}")
                    speedy_urls.append(proxy['url'])
                    counter += 1
                else:
                    logger.debug(f"Proxy {proxy['url']} timed out")
                if counter >= SCRAPING_BATCH_SIZE:
                    logger.info('Found enough fast proxies')
                    break
        yield speedy_urls


def verify_proxy_speed(url):
    try:
        response = requests.head('https://www.linkedin.com/',
                                 timeout=VERIFY_SPEED_TIMEOUT_SEC,
                                 proxies=dict(http=url, https=url))
        speed_sec = int(response.elapsed.total_seconds())
    except:
        speed_sec = 1000
    return dict(url=url, speed_sec=speed_sec)
