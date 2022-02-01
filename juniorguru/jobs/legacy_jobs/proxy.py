import random

from scrapy.downloadermiddlewares.retry import RetryMiddleware

from juniorguru.lib import loggers
from juniorguru.models import Proxy, db


logger = loggers.get(__name__)


USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Mozilla/5.0 (iPhone; CPU OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/29.0 Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
]


class ScrapingProxyMiddleware():
    EXCEPTIONS_TO_RETRY = RetryMiddleware.EXCEPTIONS_TO_RETRY

    @classmethod
    def from_crawler(cls, crawler):
        with db:
            proxies = [proxy.address for proxy in Proxy.listing()]
        return cls(proxies, crawler.settings)

    def __init__(self, proxies, settings):
        self.proxies = proxies

    def get_proxy(self):
        return random.choice(self.proxies[:5]) if self.proxies else None

    def get_user_agent(self):
        return random.choice(USER_AGENTS)

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
