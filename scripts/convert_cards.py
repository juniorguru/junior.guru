import sys
from pathlib import Path

from lxml import html


el = html.fromstring(Path(sys.argv[1]).read_text())

for list_el in el.cssselect('.list'):
    print('<div class="link-cards">')
    for item_el in list_el.xpath('li'):
        title = item_el.cssselect('h3,h4')[0].text_content()
        image_filename = item_el.cssselect('img')[0].get('src') \
            .split('/')[-1] \
            .replace(".jpg') }}", '.jpg')
        url = item_el.cssselect('a')[0].get('href')

        try:
            text = html.tostring(item_el.cssselect('p')[0], encoding='utf-8') \
                .decode('utf-8') \
                .replace('<p>', '') \
                .replace('</p>', '') \
                .strip()
        except IndexError:
            text = ''

        print('\n'.join([
            f"  {{{{ link_card(",  # noqa
            f"    '{title}',",
            f"    '{image_filename}',",
            f"    '{url}',",
            f"    '{text}'",
            f"  ) }}}}",  # noqa
        ]))
    print('</div>')
