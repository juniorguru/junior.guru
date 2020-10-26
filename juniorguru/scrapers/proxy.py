import os

from stem import Signal
from stem.control import Controller
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

from juniorguru.lib.log import get_log


ENABLE_PROXY = bool(os.getenv('ENABLE_PROXY', False))


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
        return response


def is_proxied_request(spider):
    if not ENABLE_PROXY:
        return False
    return getattr(spider, 'proxy', False)


def new_tor_identity():
    with Controller.from_port(port=9051) as controller:
        # TODO controller.authenticate(password='PASSWORDHERE')
        controller.signal(Signal.NEWNYM)
