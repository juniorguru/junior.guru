import favicon


class Pipeline():
    def process_item(self, item, spider):
        if not item.get('company_logo_urls'):
            item['company_logo_urls'] = get_favicons(item.get('company_link'))
        return item


def get_favicons(link):
    try:
        return unique(icon.url for icon in favicon.get(link))
    except:
        return []


def unique(iterable):
    return list(frozenset(filter(None, iterable)))
