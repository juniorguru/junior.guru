from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


UTM_PARAM_NAMES = ["utm_source", "utm_medium", "utm_campaign"]


def strip_params(url, param_names):
    parts = urlparse(url)
    params = {
        name: value
        for name, value in parse_qs(parts.query).items()
        if name not in param_names
    }
    query = urlencode(params, doseq=True)
    return urlunparse(parts._replace(query=query))


def strip_utm_params(url):
    return strip_params(url, UTM_PARAM_NAMES)
