import re

from juniorguru.sync.jobs_scraped.processing import DropItem


RE_IDENTIFY_MAPPING = [
    ('juniorguru', re.compile(r'\bjunior\.guru/jobs/(?P<id>[0-9a-fA-F]+)', re.I)),
    ('startupjobs', re.compile(r'\bstartupjobs\.cz/nabidka/(?P<id>\d+)', re.I)),
    ('remoteok', re.compile(r'\bremoteok\.io/remote-jobs/(?P<id>\d+)', re.I)),
    ('weworkremotely', re.compile(r'\bweworkremotely\.com/remote-jobs/(?P<id>[\w+\-]+)', re.I)),
    ('stackoverflow', re.compile(r'\bstackoverflow\.com/jobs/(?P<id>\d+)', re.I)),
    ('linkedin', re.compile(r'\blinkedin\.com/jobs/view/[\w+\-%]+\-(?P<id>\d+)', re.I)),
]


class MissingIdentifyingField(DropItem):
    pass


def process(item):
    try:
        url = item['url']
    except KeyError as e:
        raise MissingIdentifyingField(str(e))

    item['boards_ids'] = parse_urls(filter(None, [url, item.get('apply_url')]))
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
