import favicon


class Pipeline():
    def process_item(self, item, spider):
        if spider.name != 'juniorguru':
            return item  # TODO temporary

        if not item.get('image_urls'):
            item['image_urls'] = get_favicons(item.get('company_link'))
        return item


def get_favicons(link):
    try:
        return unique(icon.url for icon in favicon.get(link))
    except:
        return []


def unique(iterable):
    return list(frozenset(filter(None, iterable)))
