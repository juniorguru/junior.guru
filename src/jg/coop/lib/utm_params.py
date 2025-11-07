from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


UTM_PARAM_NAMES = [
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term",
]


def strip_params(url: str, param_names: list[str]) -> str:
    parts = urlparse(url)
    params = {
        name: value
        for name, value in parse_qs(parts.query).items()
        if name not in param_names
    }
    query = urlencode(params, doseq=True)
    return urlunparse(parts._replace(query=query))


def strip_utm_params(url: str) -> str:
    return strip_params(url, UTM_PARAM_NAMES)


def get_utm_params(url: str) -> dict[str, str]:
    parts = urlparse(url)
    params = parse_qs(parts.query)
    return {
        name: params[name][0]
        for name in UTM_PARAM_NAMES
        if params.get(name)
    }


def put_utm_params(url: str, utm_params: dict[str, str]) -> str:
    parts = urlparse(url)
    params = parse_qs(parts.query)
    for name, value in utm_params.items():
        params[name] = [value]
    query = urlencode(params, doseq=True)
    return urlunparse(parts._replace(query=query))
