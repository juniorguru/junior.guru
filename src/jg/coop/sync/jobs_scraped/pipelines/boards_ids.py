import re

from jg.coop.sync.jobs_scraped import DropItem


RE_IDENTIFY_MAPPING = [
    ("juniorguru", re.compile(r"\bjunior\.guru/jobs/(?P<id>[0-9a-fA-F]+)", re.I)),
    ("startupjobs", re.compile(r"\bstartupjobs\.cz/nabidka/(?P<id>\d+)", re.I)),
    (
        "remoteok",
        re.compile(
            r"\bremoteok\.(com|io)/remote-jobs/([\w\-]+\-)?(?P<id>\d+)/?$", re.I
        ),
    ),
    (
        "weworkremotely",
        re.compile(r"\bweworkremotely\.com/remote-jobs/(?P<id>[\w+\-]+)", re.I),
    ),
    (
        "linkedin",
        re.compile(r"\blinkedin\.com/jobs/view/([\w+\-%]+\-)?(?P<id>\d+)", re.I),
    ),
    ("jobscz", re.compile(r"\bwww\.jobs\.cz/rpd/(?P<id>\d+)", re.I)),
    ("jobscz", re.compile(r"\bwww\.jobs\.cz/fp/[^/]+/(?P<id>\d+)", re.I)),
    ("jobscz", re.compile(r"\.jobs\.cz/detail-pozice.*[\&\?]id=(?P<id>\d+)", re.I)),
]


async def process(item: dict) -> dict:
    try:
        url = item["url"]
    except KeyError as e:
        raise DropItem(str(e))

    urls = filter(None, item.get("source_urls", []) + [url, item.get("apply_url")])
    item["boards_ids"] = parse_urls(urls)
    return item


def parse_urls(urls):
    boards_ids = filter(None, map(parse_url, urls))
    return sorted(set(boards_ids))


def parse_url(url):
    for namespace, re_id in RE_IDENTIFY_MAPPING:
        match = re_id.search(url)
        if match:
            return f"{namespace}#{match.group('id')}"
    return None
