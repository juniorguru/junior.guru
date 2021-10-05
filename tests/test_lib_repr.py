from scrapy import Item, Field

from juniorguru.lib.repr import repr_item


class ExampleItem(Item):
    title = Field()
    something = Field()
    boo = Field()
    not_important = Field()

    def __repr__(self):
        return repr_item(self, ['title', 'something', 'boo'])


def test_repr_item():
    item = ExampleItem(title='Fabulous\' Item',
                       something=123,
                       boo=True,
                       not_important=890)
    assert str(item) == (
        "test_lib_repr.ExampleItem(\n"
        "    title=\"Fabulous' Item\",\n"
        "    something=123,\n"
        "    boo=True,\n"
        "    [4 fields in total]\n"
        ")"
    )


def test_repr_item_no_remaining_fields():
    item = ExampleItem(title='Fabulous\' Item',
                       something=123,
                       boo=True)
    assert str(item) == (
        "test_lib_repr.ExampleItem(\n"
        "    title=\"Fabulous' Item\",\n"
        "    something=123,\n"
        "    boo=True\n"
        ")"
    )
