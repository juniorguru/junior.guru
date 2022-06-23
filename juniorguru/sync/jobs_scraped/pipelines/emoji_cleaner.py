import emoji


def process(item):
    item['title'] = emoji.replace_emoji(item['title'], replace='').strip()
    return item
