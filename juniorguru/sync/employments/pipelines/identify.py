import re

from scrapy.exceptions import DropItem


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


class Pipeline():
    def process_item(self, item, spider):
        try:
            urls = [item['url'], item.get('apply_url')]
        except KeyError as exc:
            raise MissingIdentifyingField(str(exc))

        item['external_ids'] = sorted(set([parse_id(url) for url in urls if url]))
        return item


def parse_id(url):
    for namespace, re_id in RE_IDENTIFY_MAPPING:
        match = re_id.search(url)
        if match:
            return f"{namespace}#{match.group('id')}"
    return None
