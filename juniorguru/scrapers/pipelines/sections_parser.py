import re

from lxml import html
from w3lib.html import remove_tags


class Pipeline():
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Block-level_elements#Elements
    block_element_names = [
        'address', 'article', 'aside', 'blockquote', 'details', 'dialog',
        'dd', 'div', 'dl', 'dt', 'fieldset', 'figcaption', 'figure', 'footer',
        'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hgroup', 'hr',
        'li', 'main', 'nav', 'ol', 'p', 'pre', 'section', 'table', 'ul',
    ]
    newline_element_names = block_element_names + ['br']
    min_bullets = 2

    def process_item(self, item, spider):
        html_tree = html.fromstring(item['description_raw'])
        sections = [self.parse_list_el(list_el)
                    for list_el in html_tree.cssselect('ul, ol')]
        print(repr(list(self.parse_textual_lists(html_tree))))
        item['sections'] = sections
        return item

    def parse_list_el(self, list_el):
        # get first textual node (either tail or text content) before the list
        # and pronounce it to be the list header
        heading = None
        el = list_el.getprevious()
        while el is not None:
            tail_text = el.tail.strip() if el.tail else ''
            if tail_text:
                heading = tail_text
                break

            text = el.text_content().strip()
            if text:
                heading = text
                break

            el = el.getprevious()

        # pronounce text content of all the list items to be bullets;
        # any tail texts are treated just as list items
        bullets = []
        for li_el in list_el.cssselect('li'):
            bullets.append(li_el.text_content().strip())
            tail_text = li_el.tail.strip() if li_el.tail else ''
            if tail_text:
                bullets.append(tail_text)

        return dict(heading=heading, bullets=bullets)

    def parse_textual_lists(self, el):
        # iterate over all elements which visually imply newline when rendered
        # in the browser and add the newline explicitly to their tail
        for newline_el in el.cssselect(', '.join(self.newline_element_names)):
            tail_text = newline_el.tail
            newline_el.tail = f'\n{tail_text}' if tail_text else '\n'

        # TODO remove whitespace prior to adding our own???

        # serialize the html tree and remove tags, but keep all whitespace
        # as it was so we know where the visual newlines are, then split lines
        html_text = html.tostring(el, encoding=str)
        text = remove_tags(html_text)
        text = re.sub(r'[\n\r]+', '\n', text.strip())
        lines = text.splitlines()

        # iterate over lines, detect bullet characters (line prefix), and
        # construct lists with headings
        bullets = []
        previous_prefix = None

        for line in lines:
            flush = False
            split = re.split(r'\s+', line, maxsplit=1)

            if len(split) == 1:  # rogue prefix-only line
                prefix = split[0]
                if prefix == previous_prefix:  # next list item: skip
                    continue
                else:  # anything but next list item: flush & skip
                    if len(bullets) >= self.min_bullets:
                        yield dict(bullets=bullets)
                    bullets = []
            else:  # regular line
                prefix, line_reminder = split
                if prefix == previous_prefix:  # next list item: add
                    bullets.append(line_reminder)
                else:  # anything but next list item: flush & add
                    if len(bullets) >= self.min_bullets:
                        yield dict(bullets=bullets)
                    bullets = [line_reminder]

            previous_prefix = prefix

        if len(bullets) >= self.min_bullets:
            yield dict(bullets=bullets)
