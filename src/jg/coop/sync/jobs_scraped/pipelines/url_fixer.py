from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


async def process(item: dict) -> dict:
    item["url"] = fix_url(item.get("url"))
    item["apply_url"] = fix_url(item.get("apply_url"))
    item["company_url"] = fix_url(item.get("company_url"))
    item["company_logo_urls"] = [
        fix_url(url) for url in item.get("company_logo_urls", [])
    ]
    item["source_urls"] = [fix_url(url) for url in item.get("source_urls", [])]
    return item


def fix_url(url: str) -> str:
    if not url:
        return None
    url = url.strip()
    if not url.startswith("http"):
        return f"https://{url}"
    return url
