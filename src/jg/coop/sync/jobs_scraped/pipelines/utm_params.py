from collections import defaultdict
from pprint import pformat

from jg.coop.lib.job_urls import get_all_urls
from jg.coop.lib.utm_params import get_utm_params, put_utm_params


async def process(item: dict) -> dict:
    utm_params = defaultdict(set)
    for url in get_all_urls(item):
        for name, value in get_utm_params(url).items():
            utm_params[name].add(value)
    utm_params["utm_source"] = {"juniorguru"}
    utm_params = {
        name: values.pop() for name, values in utm_params.items() if len(values) == 1
    }
    utm_params = dict(sorted(utm_params.items()))  # deterministic order for tests

    try:
        canonical_url = item["url"]
    except KeyError:
        raise ValueError(f"Item has no URLs:\n{pformat(item)}")
    item["url"] = put_utm_params(canonical_url, utm_params)
    return item
