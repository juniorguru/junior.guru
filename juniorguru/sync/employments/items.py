from scrapy import Field, Item


class Employment(Item):
    title = Field()
    company_name = Field()
    url = Field()
    apply_url = Field()
    external_ids = Field()
    locations = Field()
    remote = Field()
    lang = Field()
    description_html = Field()
    seen_at = Field()
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
