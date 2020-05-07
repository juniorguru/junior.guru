from scrapy.exceptions import DropItem

from juniorguru.scrapers.items import Job


class MissingRequiredFields(DropItem):
    pass


class Pipeline():
    required_fields = {name for name, kwargs in Job.fields.items()
                       if kwargs.get('required') is True}

    def process_item(self, item, spider):
        missing_fields = self.required_fields - frozenset(item.keys())
        if missing_fields:
            missing_fields = sorted(missing_fields)
            raise MissingRequiredFields(f"Missing: {', '.join(missing_fields)}")
        return item
