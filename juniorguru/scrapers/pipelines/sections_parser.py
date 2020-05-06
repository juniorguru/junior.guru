from lxml import html


class Pipeline():
    def process_item(self, item, spider):
        html_tree = html.fromstring(item['description_raw'])
        sections = [self.process_list_el(list_el)
                    for list_el in html_tree.cssselect('ul, ol')]
        item['sections'] = sections
        return item

    def process_list_el(self, list_el):
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

        bullets = []
        for li_el in list_el.cssselect('li'):
            bullets.append(li_el.text_content().strip())
            tail_text = li_el.tail.strip() if li_el.tail else ''
            if tail_text:
                bullets.append(tail_text)

        return dict(heading=heading, bullets=bullets)
