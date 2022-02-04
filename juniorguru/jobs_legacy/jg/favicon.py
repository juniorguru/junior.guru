from juniorguru.lib import loggers

import favicon


logger = loggers.get(__name__)


# https://docs.python-requests.org/en/master/user/advanced/#timeouts
FAVICON_REQUEST_TIMEOUT = (3.05, 5)

# Just copy-paste of raw headers Firefox sends to a web page. None of it is
# intentionally set to a specific value with a specific meaning.
FAVICON_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8,cs;q=0.6,sk;q=0.4,es;q=0.2',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Cache-Control': 'max-age=0',
}


class Pipeline():
    SUPPORTED_SPIDERS = ['juniorguru']

    def process_item(self, item, spider):
        # TODO detect/distinguish true company URLs even for the other job boards
        if spider.name not in self.SUPPORTED_SPIDERS:
            return item

        if not item.get('company_logo_urls') and item.get('company_url'):
            company_url = item['company_url']
            logger.debug(f"Favicon lookup at '{company_url}'")
            item['company_logo_urls'] = get_favicons(company_url)
        return item


def get_favicons(link):
    try:
        icons = favicon.get(link,
                            timeout=FAVICON_REQUEST_TIMEOUT,
                            headers=FAVICON_REQUEST_HEADERS)
        return unique(icon.url for icon in icons)
    except Exception as e:
        logger.debug(f"Favicon lookup has failed: {e}")
        return []


def unique(iterable):
    return list(frozenset(filter(None, iterable)))
