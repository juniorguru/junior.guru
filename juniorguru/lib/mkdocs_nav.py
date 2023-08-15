from typing import Generator
from mkdocs.structure.pages import Page
from mkdocs.structure import StructureItem


def get_toc(page: Page) -> Generator[dict, None, None]:
    # for pages without children, this should result in the same
    # value as page.parent, but for pages further down the tree,
    # this ensures we display only the top-level items, regardless
    # of the depth of the current page
    parents = [page]
    while parents[0].parent:
        parents.insert(0, parents[0].parent)
    parent = parents[0]

    # iterate over items
    for item in parent.children:
        if item.children:
            item_page = item.children[0]
        else:
            item_page = item

        yield dict(title=item_page.title,
                   url=item_page.url,
                   is_active=item_page == page,
                   headings=[dict(title=heading.title,
                                  url=heading.url)
                             for heading in item_page.toc])


def get_parent_page(page: Page) -> StructureItem | None:
    try:
        return page.parent.children[0]
    except AttributeError:
        return None


def get_sibling_page(page: Page, offset: int) -> StructureItem | None:
    try:
        index = page.parent.children.index(page)
        sibling_index = max(index + offset, 0)
        if index == sibling_index:
            return None
        return page.parent.children[sibling_index]
    except (AttributeError, IndexError):
        return None
