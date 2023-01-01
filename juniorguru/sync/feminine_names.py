import unicodedata

import requests
from lxml import html

from juniorguru.cli.sync import main as cli
from juniorguru.models.base import db
from juniorguru.models.feminine_name import FeminineName
from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


WIKI_URL = 'https://cs.wikipedia.org/wiki/Seznam_nej%C4%8Dast%C4%9Bj%C5%A1%C3%ADch_%C5%BEensk%C3%BDch_jmen_v_%C4%8Cesku'

EXTRA_NAMES = [
    'Kayla', 'Hannah', 'Alisa', 'Hany', 'Evgenia', 'Kate', 'Lindice',
    'Anastasija', 'Anastassiya', 'Nataliya', 'Dinara', 'Eleanor',
    'Darja', 'Tina', 'Katarína', 'Lívia',
]


@cli.sync_command()
@db.connection_context()
def main():
    FeminineName.drop_table()
    FeminineName.create_table()

    response = requests.get(WIKI_URL)
    response.raise_for_status()
    html_tree = html.fromstring(response.content)

    names = [element.text_content().strip()
             for element
             in html_tree.cssselect('.wikitable a[href]')] + EXTRA_NAMES

    for name in names:
        name_lower = name.lower()
        name_ascii = remove_accents(name_lower)
        logger.info(f'{name} → {name_lower}, {name_ascii}')
        FeminineName \
            .insert_many([
                dict(name=name_lower),
                dict(name=name_ascii),
            ]) \
            .on_conflict_ignore() \
            .execute()


def remove_accents(s):
    # https://stackoverflow.com/a/518232/325365
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')
