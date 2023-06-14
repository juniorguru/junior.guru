from scrapy import Field, Item

from juniorguru.lib.repr import repr_item


class EmploymentItem(Item):
    title = Field()
    company_name = Field()
    url = Field()
    apply_url = Field()
    external_ids = Field()
    locations = Field()
    remote = Field()
    lang = Field()
    description_html = Field()
    description_text = Field()
    first_seen_at = Field()
    last_seen_at = Field()
    employment_types = Field()

    # juniority
    juniority_re_score = Field()
    juniority_ai_opinion = Field()
    juniority_votes_score = Field()
    juniority_votes_count = Field()

    # meta information
    source = Field()
    source_urls = Field()
    adapter = Field()
    build_url = Field()

    def __repr__(self):
        return repr_item(self, ['title', 'url', 'apply_url', 'source', 'adapter'])
