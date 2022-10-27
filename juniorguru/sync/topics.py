import re
from collections import Counter

import click

from juniorguru.lib import loggers
from juniorguru.cli.sync import Command
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.topic import Topic


logger = loggers.get(__name__)


KEYWORDS = {re.compile(r'\b' + key + r'\b', re.IGNORECASE): value for key, value in {
    r'pyladies|pylady': 'pyladies',
    r'cs50': 'cs50',
    r'enget\w+': 'engeto',
    r'czechitas': 'czechitas',
    r'(datov\w+|digit\w+) akademi\w+': 'czechitas',
    r'it[ \-]?network': 'itnetwork',
    r'react ?girls': 'reactgirls',
    r'python\w*': 'python',
    r'js': 'javascript',
    r'javascript\w*': 'javascript',
    r'aoc': 'adventofcode',
    r'advent ?of ?code': 'adventofcode',
    r'sdacademy': 'sdacademy',
    r'sda': 'sdacademy',
    r'software development a[ck]adem\w+': 'sdacademy',
    r'udemy': 'udemy',
    r'learn2code': 'skillmea',
    r'l2c': 'skillmea',
    r'skillmea': 'skillmea',
    r'prima ?kurzy': 'primakurzy',
    r'kurzy\.vsb': 'vsb',
    r'všb': 'vsb',
    r'django ?girls': 'djangogirls',
    r'coding ?boo?tcamp( pra(ha|gue))?': 'codingbootcamppraha',
    r'data4you': 'codingbootcamppraha',
    r'green ?fox( academy| akademi[ei])?': 'greenfox',
    r'gfa': 'greenfox',
    r'unicorn\w*': 'unicorn',
    r'(it\s*)?step(\.org)?': 'step',
}.items()}

TOPIC_CHANNELS = {re.compile(key): value for key, value in {
    r'^adventofcode$': 'adventofcode',
}.items()}


@click.command(cls=Command, requires=['club-content'])
@db.connection_context()
def main():
    Topic.drop_table()
    Topic.create_table()

    topics = {}
    messages = ClubMessage.listing()
    for message in messages:
        topic_channel_keyword = get_topic_channel_keyword(message.channel_name)
        if topic_channel_keyword:
            topics.setdefault(topic_channel_keyword, Counter())
            topics[topic_channel_keyword]['topic_channels_messages_count'] += 1

        for keyword_re, keyword in KEYWORDS.items():
            if keyword_re.search(message.content):
                topics.setdefault(keyword, Counter())
                topics[keyword]['mentions_count'] += 1
    for name, data in topics.items():
        logger.info(f"{name} {dict(data)}")
        Topic.create(**{'name': name, **data})


def get_topic_channel_keyword(channel_name):
    for keyword_re, keyword in TOPIC_CHANNELS.items():
        if keyword_re.search(channel_name):
            return keyword
    return None
