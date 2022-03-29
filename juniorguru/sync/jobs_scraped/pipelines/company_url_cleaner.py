import re


COMPANY_URL_RES = [re.compile(url_re, re.I) for url_re in [
    r'https?://([a-z]+\.)?linkedin\.com/company',
]]


def process(item):
    if item['company_url']:
        for url_re in COMPANY_URL_RES:
            if url_re.search(item['company_url']):
                item['company_url'] = None
                break
    return item
