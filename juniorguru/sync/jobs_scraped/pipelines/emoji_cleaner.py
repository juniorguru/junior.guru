import emoji


EMOJI_RE = emoji.get_emoji_regexp()


def process(item):
    item['title'] = EMOJI_RE.sub('', item['title']).strip()
    return item
