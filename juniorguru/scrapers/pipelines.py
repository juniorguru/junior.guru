import re
import hashlib

import langdetect
from scrapy.exceptions import DropItem

from .. import models


class GermanGenderCleaner():
    gender_re = re.compile(r'''
        \s*                     # trailing spaces
        \(                      # opening parenthesis
            \s*[mfw]\s*         # letter m, f, or w (with trailing spaces)
            /                   # slash
            \s*[mfw]\s*         # letter m, f, or w (with trailing spaces)
            (                   # optionally:
                /               # slash
                \s*[^\)]+\s*    # anything but closing bracket, one or more (with trailing spaces)
            )?
        \)                      # closing parenthesis
        \s*                     # trailing spaces
    ''', re.VERBOSE | re.IGNORECASE)

    def process_item(self, item, spider):
        item['title'] = self.gender_re.sub(' ', item['title']).strip()
        return item


class LanguageFilter():
    relevant_langs = ['cs', 'sk', 'en']

    def process_item(self, item, spider):
        lang = langdetect.detect(item['description_raw'])
        if lang not in self.relevant_langs:
            raise DropItem(f"Language detected as '{lang}' (relevant: {', '.join(self.relevant_langs)})")
        item['lang'] = lang
        return item


class Database():
    def __init__(self, db=None, job_cls=None, stats=None):
        self.db = db or models.db
        self.job_cls = job_cls or models.Job
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

    def open_spider(self, spider):
        self.db.connect()

    def process_item(self, item, spider):
        self.job_cls.create(**prepare_job_data(item, spider.name))
        if self.stats:
            self.stats.inc_value('item_saved_count')
        return item

    def close_spider(self, spider):
        self.db.close()


def prepare_job_data(item, spider_name):
    return dict(
        **item,
        id=hashlib.sha224(item['link'].encode()).hexdigest(),
        source=spider_name,
        # is_approved=True,
    )
