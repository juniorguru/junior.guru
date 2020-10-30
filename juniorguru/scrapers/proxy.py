import random

from scrapy.core.downloader.handlers.http11 import TunnelError

from juniorguru.lib.log import get_log


log = get_log(__name__)


# TODO
# https://github.com/clarketm/proxy-list
# https://github.com/imWildCat/scylla


# TODO do this in a better way
# http://free-proxy.cz/cs/proxylist/country/all/https/uptime/level1
PROXIES = [f'https://{proxy}' for proxy in '''
103.87.171.236:32582
185.248.151.139:80
175.112.89.171:3128
82.200.233.4:3128
100.25.221.97:3128
104.131.28.8:80
14.63.228.217:80
167.172.109.12:33077
161.35.122.140:3128
52.76.232.232:80
157.245.231.155:80
211.239.170.96:80
14.143.168.230:8080
62.210.69.176:5566
178.128.127.59:8080
27.133.235.144:3128
159.65.189.75:80
54.254.161.72:8888
132.145.146.10:80
144.217.101.245:3129
103.83.36.124:3838
132.145.130.198:80
162.248.243.18:3838
95.179.159.1:3128
34.64.114.171:80
74.126.83.200:80
103.92.225.98:55443
13.126.200.204:80
192.227.108.83:80
129.213.183.152:80
203.212.70.77:80
212.200.246.24:80
3.6.220.71:80
198.50.163.192:3129
178.136.2.208:55443
'''.strip().splitlines()]


USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Mozilla/5.0 (iPhone; CPU OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/29.0 Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
]


class ScrapingProxyMiddleware():
    def __init__(self, proxies=None, user_agents=None):
        self.proxies = proxies or PROXIES
        self.user_agents = user_agents or USER_AGENTS

    def get_proxy(self):
        return random.choice(self.proxies[:3]) if self.proxies else None

    def rotate_user_agent(self, headers):
        headers = {n: v for n, v in headers.items() if n.lower() != 'user-agent'}
        return {'User-Agent': random.choice(self.user_agents), **headers}

    def rotate_proxies(self, request):
        log.warning('Rotating proxies')
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
        log.warning('No proxies left, continuing without proxy')
        return request.replace(headers=self.rotate_user_agent(request.headers),
                               meta=meta,
                               dont_filter=True)

    def process_request(self, request, spider):
        if not getattr(spider, 'proxy', False):
            return
        proxy = self.get_proxy()
        if proxy:
            log.debug(f"Proxying {request!r} via {proxy} ({request.headers.get('User-Agent')})")
            request.meta['proxy'] = proxy

    def process_exception(self, request, exception, spider):
        if not getattr(spider, 'proxy', False) or not request.meta.get('proxy'):
            return
        log.debug(f'Got proxy exception {exception!r} for {request!r}')
        if isinstance(exception, TunnelError):
            return self.rotate_proxies(request)

    def process_response(self, request, response, spider):
        if not getattr(spider, 'proxy', False) or not request.meta.get('proxy'):
            return response
        if response.status in [999, 504]:
            log.info(f"Got {response!r} proxied via {request.meta['proxy']} ({request.headers.get('User-Agent')})")
            return self.rotate_proxies(request)
        log.debug(f'Got proxied response {response!r}')
        return response
