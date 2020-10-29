import random

from scrapy.core.downloader.handlers.http11 import TunnelError

from juniorguru.lib.log import get_log


log = get_log(__name__)


# TODO do this in a better way
# http://free-proxy.cz/cs/proxylist/country/all/https/uptime/level1
PROXIES = [f'https://{proxy}' for proxy in '''
165.22.81.30:45083
175.112.89.171:3128
43.250.248.254:3838
100.25.221.97:3128
140.238.84.65:3128
188.166.251.91:8086
180.92.194.235:80
18.138.49.42:80
14.143.168.230:8080
211.239.170.96:80
103.83.36.123:3838
205.147.101.141:80
132.145.146.10:80
161.35.122.140:3128
192.227.108.83:80
110.78.141.83:54181
35.214.138.103:3128
103.21.160.10:35101
13.244.75.68:80
137.74.168.93:80
187.243.255.174:8080
93.117.72.27:43631
153.126.160.91:80
103.106.148.209:30223
186.86.247.169:39168
187.62.191.3:61456
103.30.93.171:8080
195.234.87.211:53281
36.91.163.241:42734
5.141.86.107:55528
178.47.139.151:35102
202.166.207.218:56576
180.183.244.143:80
117.102.87.138:41757
125.26.99.185:36525
'''.strip().splitlines()]


class ScrapingProxyMiddleware():
    def __init__(self, proxies=None):
        self.proxies = proxies or PROXIES
        if not self.proxies:
            raise ValueError('No proxies')

    def get_proxy(self):
        return random.choice(self.proxies[:3]) if self.proxies else None

    def rotate_proxies(self, request):
        log.warning('Rotating proxies')
        meta = {k: v for k, v in request.meta.items() if k != 'proxy'}
        try:
            self.proxies.remove(request.meta.get('proxy'))
        except ValueError:
            pass
        proxy = self.get_proxy()
        if proxy:
            return request.replace(meta={'proxy': proxy, **meta}, dont_filter=True)
        log.warning('No proxies left, continuing without proxy')
        return request.replace(meta=meta, dont_filter=True)

    def process_request(self, request, spider):
        if not getattr(spider, 'proxy'):
            return
        proxy = self.get_proxy()
        log.debug(f'Proxying {request!r} via {proxy}')
        request.meta['proxy'] = proxy

    def process_exception(self, request, exception, spider):
        if not getattr(spider, 'proxy'):
            return
        log.debug(f'Got proxy exception {exception!r} for {request!r}')
        if isinstance(exception, TunnelError):
            return self.rotate_proxies(request)

    def process_response(self, request, response, spider):
        if not getattr(spider, 'proxy'):
            return response
        if response.status in [999, 504]:
            log.info(f"Got status {response.status} for {request!r} proxied via {request.meta.get('proxy', 'no proxy')}")
            return self.rotate_proxies(request)
        log.debug(f'Got proxied response {response!r} for {request!r}')
        return response
