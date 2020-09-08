import re

import requests


class MailChimpClient():
    # Useful links:
    #
    # https://mailchimp.com/help/about-api-keys/
    # https://mailchimp.com/developer/guides/get-started-with-mailchimp-api-3/
    # https://mailchimp.com/developer/reference/

    url_base = 'https://us3.api.mailchimp.com/3.0'

    def __init__(self, api_key):
        self.api_key = api_key

    def get(self, url, count=1000):
        if not url.startswith('http'):
            url = self.url_base + url
        params = {}
        if count is not None:
            params['count'] = count
        response = requests.get(url, params=params, auth=('jg', self.api_key))
        response.raise_for_status()
        return response.json()


def get_collection(data, collection):
    count = len(data[collection])
    total_count = data['total_items']
    if count != total_count:
        url = get_link(data, 'self')
        raise NotImplementedError(f'Pagination needed: {count}/{total_count}'
                                  f' {collection} ({url})')
    return data[collection]


def get_link(data, rel):
    return [link['href'] for link in data['_links'] if link['rel'] == rel][0]


def sum_clicks_per_url(urls_clicked, metric_name):
    clicks = {}
    for url_clicked in urls_clicked:
        clicks.setdefault(url_clicked['url'], 0)
        clicks[url_clicked['url']] += url_clicked[metric_name]
    return {url: sum for url, sum in clicks.items() if sum > 0}


def sum_clicks_per_external_url(*args, **kwargs):
    return {url: value for url, value in
            sum_clicks_per_url(*args, **kwargs).items()
            if is_external_url(url)}


def is_external_url(url):
    return not re.match(r'https?://junior.guru', url)
