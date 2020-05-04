import re
import string
import hashlib

import langdetect
from scrapy.exceptions import DropItem

from ..models import db as default_db, Job


class BannedWordInTitle(DropItem):
    pass


class JuniorTitleFilter():
    banned_words = ['senior', 'practiced']
    puctuation_trans_table = str.maketrans('', '', string.punctuation)

    def process_item(self, item, spider):
        words = (word.lower().translate(self.puctuation_trans_table)
                 for word in item['title'].split())
        for word in words:
            if word in self.banned_words:
                raise BannedWordInTitle(f"The title contains a banned word: '{word}'")
        return item


class EmploymentTypesCleaner():
    clean_re = re.compile(r'[\-\s]+')
    types_mapping = {
        'fulltime': 'full-time',
        'full time': 'full-time',
        'parttime': 'part-time',
        'part time': 'part-time',
        'contract': 'contract',
        'external collaboration': 'contract',
        'internship': 'internship',
    }

    def process_item(self, item, spider):
        types = (t.lower() for t in item['employment_types'])
        types = (self.types_mapping.get(self.clean_re.sub(' ', t), t)
                 for t in types)
        item['employment_types'] = list(frozenset(types))
        return item


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


class IrrelevantLanguage(DropItem):
    pass


class LanguageFilter():
    relevant_langs = ['cs', 'sk', 'en']

    def process_item(self, item, spider):
        lang = langdetect.detect(item['description_raw'])
        if lang not in self.relevant_langs:
            raise IrrelevantLanguage(f"Language detected as '{lang}' (relevant: {', '.join(self.relevant_langs)})")
        item['lang'] = lang
        return item


class Database():
    def __init__(self, db=None, model=None, stats=None):
        self.db = db or default_db
        self.model = model or Job
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

    def process_item(self, item, spider):
        with self.db:
            self.model.create(**prepare_job_data(item, spider.name))
        if self.stats:
            self.stats.inc_value('item_saved_count')
        return item


def item_to_job_id(item):
    return hashlib.sha224(item['link'].encode()).hexdigest()


def prepare_job_data(item, spider_name):
    return dict(
        **item,
        id=item_to_job_id(item),
        source=spider_name,
        # is_approved=True,
    )
