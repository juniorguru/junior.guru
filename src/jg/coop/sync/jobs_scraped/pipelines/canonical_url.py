from pprint import pformat

from jg.coop.lib.job_urls import get_all_urls, id_to_url, urls_to_ids


async def process(item: dict) -> dict:
    if urls := get_all_urls(item):
        url = item["url"]
        source_urls = item.get("source_urls", [])
        if canonical_ids := urls_to_ids(urls):
            item["url"] = id_to_url(canonical_ids[0])
            item["source_urls"] = sorted(set(source_urls + [url]))
            item["canonical_ids"] = canonical_ids
            return item
        raise NotImplementedError(f"No canonical IDs from URLs: {urls}")
    raise ValueError(f"Item has no URLs:\n{pformat(item)}")
