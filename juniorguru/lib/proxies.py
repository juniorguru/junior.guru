from pathlib import Path
import random

from scrapy.downloadermiddlewares.retry import RetryMiddleware

from juniorguru.lib import loggers


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
        return cls(PROXIES_PATH.read_text().splitlines(),
                   enabled=crawler.settings.getbool('PROXIES_ENABLED'),
                   user_agents=crawler.settings.getlist('PROXIES_USER_AGENTS'))

    def __init__(self, proxies, enabled=False, user_agents=None):
        self.enabled = enabled
        self.user_agents = user_agents or self.DEFAULT_PROXIES_USER_AGENTS
        self.proxies = proxies
        self.priority_proxies = []

    def get_proxy(self):
        try:
            return random.choice(self.priority_proxies)
        except IndexError:
            try:
                return random.choice(self.proxies)
            except IndexError:
                return None

    def get_user_agent(self):
        return random.choice(self.user_agents)

    def rotate_user_agent(self, headers):
        headers = {n: v for n, v in headers.items() if n.lower() != 'user-agent'}
        return {'User-Agent': self.get_user_agent(), **headers}

    def prioritize_proxy(self, proxy_url):
        try:
            self.proxies.remove(proxy_url)
        except ValueError:
            pass
        self.priority_proxies.append(proxy_url)

    def rotate_proxies(self, request):
        logger.warning(f'Rotating proxies (currently {len(self.proxies)})')
        meta = {k: v for k, v in request.meta.items() if k != 'proxy'}

        proxy_url = request.meta.get('proxy')
        try:
            self.proxies.remove(proxy_url)
        except ValueError:
            pass
        try:
            self.priority_proxies.remove(proxy_url)
        except ValueError:
            pass

        proxy_url = self.get_proxy()
        if proxy_url:
            return request.replace(headers=self.rotate_user_agent(request.headers),
                                   meta={'proxy': proxy_url, **meta},
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
        proxy_url = self.get_proxy()
        if proxy_url:
            logger.debug(f"Proxying {request!r} via {proxy_url} ({user_agent})")
            request.meta['proxy'] = proxy_url

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
            return response
        proxy_url = request.meta['proxy']
        if response.status in [504, 999]:
            user_agent = request.headers.get('User-Agent').decode()
            logger.info(f"Got {response!r} proxied via {proxy_url} ({user_agent})")
            return self.rotate_proxies(request)
        logger.debug(f'Got proxied response {response!r}')
        self.prioritize_proxy(proxy_url)
        return response
