import emoji


class Pipeline():
    emoji_re = emoji.get_emoji_regexp()

    def process_item(self, item, spider):
        item['title'] = self.emoji_re.sub('', item['title']).strip()
        return item
