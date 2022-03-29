from functools import lru_cache

from scrapy.exceptions import DropItem


class MissingRequiredFields(DropItem):
    pass


class Pipeline():
    def process_item(self, item, spider):
        required_fields = get_required_fields(item.__class__)
        missing_fields = required_fields - frozenset(item.keys())
        if missing_fields:
            missing_fields = sorted(missing_fields)
            raise MissingRequiredFields(f"Missing: {', '.join(missing_fields)}")
        return item


@lru_cache()
def get_required_fields(cls):
    return {name for name, kwargs in cls.fields.items()
            if kwargs.get('required') is True}
