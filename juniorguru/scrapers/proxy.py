import os

from stem import Signal
from stem.control import Controller
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

from juniorguru.lib.log import get_log


PROXY_ENABLED = bool(os.getenv('PROXY_ENABLED', False))


log = get_log(__name__)


class ProxyMiddleware(HttpProxyMiddleware):
    def process_request(self, request, spider):
        if is_proxied_request(spider):
            # TODO new_tor_identity()
            log.warning(f'Sending proxied request to {request!r}')
            request.meta['proxy'] = 'http://127.0.0.1:8118'

    def process_response(self, request, response, spider):
        if response.status == 999:
            log.warning(f'Request {request!r} blocked!')
            if is_proxied_request(spider):
                log.warning(f'Retrying {request!r} with different identity')
                new_tor_identity()
                return request
            else:
                log.warning(f'Request {request!r} blocked but oh oh oh not proxied! PROXY_ENABLED={PROXY_ENABLED} spider.proxy={spider.proxy}')
        return response


def is_proxied_request(spider):
    return getattr(spider, 'proxy', False) if PROXY_ENABLED else False


def new_tor_identity():
    with Controller.from_port(port=9051) as controller:
        # TODO controller.authenticate(password='PASSWORDHERE')
        controller.signal(Signal.NEWNYM)
