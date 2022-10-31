import random
from pathlib import Path

from scrapy.downloadermiddlewares.retry import RetryMiddleware

from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


class ScrapingProxiesMiddleware():
    EXCEPTIONS_TO_RETRY = RetryMiddleware.EXCEPTIONS_TO_RETRY

    DEFAULT_PROXIES_USER_AGENTS = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Mozilla/5.0 (iPhone; CPU OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/29.0 Mobile/15E148 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0',
    ]

    @classmethod
    def from_crawler(cls, crawler):
        proxies_list_path = Path(crawler.settings.get('PROXIES_FILE'))
        proxies_list = proxies_list_path.read_text().splitlines()
        return cls(proxies_list,
                   user_agents=crawler.settings.getlist('PROXIES_USER_AGENTS'))

    def __init__(self, proxies, user_agents=None):
        self.user_agents = user_agents or self.DEFAULT_PROXIES_USER_AGENTS
        self.proxies = {proxy_url: None for proxy_url in proxies}

    def get_proxy(self):
        used_proxies = {proxy_url: latency for proxy_url, latency
                            in self.proxies.items() if latency is not None}
        logger.info(f"Total {len(self.proxies)} proxies, {len(used_proxies)} in use")

        try:
            unused_proxies = [next(proxy_url for proxy_url in self.proxies.keys()
                                   if proxy_url not in used_proxies)]
        except StopIteration:
            unused_proxies = []
        proxies = list(used_proxies.keys()) + unused_proxies

        try:
            return random.choice(proxies)
        except IndexError:
            return None

    def get_user_agent(self):
        return random.choice(self.user_agents)

    def rotate_user_agent(self, headers):
        headers = {n: v for n, v in headers.items() if n.lower() != 'user-agent'}
        return {'User-Agent': self.get_user_agent(), **headers}

    def record_proxy_latency(self, proxy_url, latency):
        self.proxies[proxy_url] = latency

    def rotate_proxies(self, request):
        prev_proxy_url = request.meta.get('proxy')

        try:
            prev_latency = self.proxies[prev_proxy_url]
        except KeyError:
            pass
        else:
            if prev_latency is None:
                del self.proxies[prev_proxy_url]
            else:
                next_latency = request.meta.get('download_latency', request.meta['download_timeout'])
                self.proxies[prev_proxy_url] = next_latency

        next_proxy_url = self.get_proxy()
        meta = {k: v for k, v in request.meta.items() if k != 'proxy'}
        if next_proxy_url:
            logger.debug(f'Rotating proxies: {next_proxy_url} instead of {prev_proxy_url}')
            return request.replace(headers=self.rotate_user_agent(request.headers),
                                   meta={'proxy': next_proxy_url, **meta},
                                   dont_filter=True)
        logger.warning('No proxies, continuing without proxy')
        return request.replace(headers=self.rotate_user_agent(request.headers),
                               meta=meta,
                               dont_filter=True)

    def process_request(self, request, spider):
        if not getattr(spider, 'proxies', False):
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
        if not getattr(spider, 'proxies', False):
            return
        if not request.meta.get('proxy'):  # proxies haven't been used for this request
            return
        logger.debug(f'Got proxy exception {exception!r} for {request!r}')
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            return self.rotate_proxies(request)

    def process_response(self, request, response, spider):
        if not getattr(spider, 'proxies', False):
            return response
        if not request.meta.get('proxy'):  # proxies haven't been used for this request
            return response
        proxy_url = request.meta['proxy']
        if self.is_invalid_response(response):
            user_agent = request.headers.get('User-Agent').decode()
            logger.info(f"Invalid response: {response!r} proxied via {proxy_url} ({user_agent})")
            return self.rotate_proxies(request)
        logger.debug(f'Got proxied response {response!r}')
        self.record_proxy_latency(proxy_url, request.meta.get('download_latency', 0))  # requests from cache don't have this set
        return response

    def is_invalid_response(self, response):
        return response.status in [504, 999]
