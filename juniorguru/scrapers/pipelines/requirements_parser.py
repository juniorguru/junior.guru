from scrapy.selector import Selector


class Pipeline():
    heading_elements = ['strong']
    heading_keywords = ['knowledge and experience']

    def process_item(self, item, spider):
        description_sel = Selector(text=item['description_raw'])

        requirements = []
        for list_sel in description_sel.css('ul, ol'):
            heading_sel = self.find_heading(list_sel)
            if heading_sel:
                heading_text = self.extract_text(heading_sel).lower()
                for keyword in self.heading_keywords:
                    if keyword in heading_text:
                        for item_sel in list_sel.css('li'):
                            requirements.append(self.extract_text(item_sel))

        item['requirements'] = requirements
        return item

    def find_heading(self, list_sel):
        criteria = ' or '.join([f'self::{name}' for name
                                in self.heading_elements])
        headings = list_sel.xpath(f'./preceding-sibling::*[{criteria}][1]')
        try:
            return headings[0]
        except IndexError:
            return None

    def extract_text(self, sel):
        return ' '.join(sel.xpath('.//text()').getall()).strip()
