from pprint import pformat

from jg.coop.lib.job_urls import id_to_url, urls_to_ids


async def process(item: dict) -> dict:
    try:
        url = item["url"]
    except KeyError:
        raise RuntimeError(f"Item has no URL:\n{pformat(item)}")

    source_urls = item.get("source_urls", [])
    urls = source_urls + [url, item.get("apply_url")]
    urls = list(filter(None, urls))
    canonical_ids = urls_to_ids(urls)

    if not canonical_ids:
        raise NotImplementedError(f"Could not parse canonical IDs from URLs: {urls}")

    item["url"] = id_to_url(canonical_ids[0])
    item["source_urls"] = sorted(set(source_urls + [url]))
    item["canonical_ids"] = canonical_ids
    return item
