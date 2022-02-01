from juniorguru.jobs.legacy_jobs.pipelines.description_parser import extract_text


class Pipeline():
    def process_item(self, item, spider):
        if item.get('description_html'):
            description_text = extract_text(item['description_html'])
            item['description_text'] = description_text
        return item
