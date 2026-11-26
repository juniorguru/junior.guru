from collections.abc import Mapping
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


UTM_PARAM_NAMES = [
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term",
]

CLUB_UTM_MEDIUM = "web"

CLUB_UTM_CAMPAIGN = "jaro"


def club_utm_params(source: str, content: str | int | None = None) -> dict[str, str]:
    """UTM params for links from the site to the club, which identify the placement"""
    utm_params = {
        "utm_source": source,
        "utm_medium": CLUB_UTM_MEDIUM,
        "utm_campaign": CLUB_UTM_CAMPAIGN,
    }
    if content is not None:
        utm_params["utm_content"] = str(content)
    return utm_params


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
    params = parse_qs(urlparse(url).query)
    return pick_utm_params({name: values[0] for name, values in params.items()})


def pick_utm_params(params: Mapping[str, str | None]) -> dict[str, str]:
    """Keeps only UTM params with non-empty values"""
    return {name: value for name in UTM_PARAM_NAMES if (value := params.get(name))}


def put_utm_params(url: str, utm_params: dict[str, str]) -> str:
    parts = urlparse(url)
    params = parse_qs(parts.query)
    for name, value in utm_params.items():
        params[name] = [value]
    query = urlencode(params, doseq=True)
    return urlunparse(parts._replace(query=query))
