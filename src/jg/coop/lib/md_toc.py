from xml.etree.ElementTree import Element

from markdown.extensions import toc


class TocTreeprocessor(toc.TocTreeprocessor):
    def add_permalink(self, c: Element, elem_id: str) -> None:
        """Skips H1, because a permalink to the top of the page is useless
        and the '#' pollutes the heading text for crawlers and screen readers
        """
        if c.tag != "h1":
            super().add_permalink(c, elem_id)


class TocExtension(toc.TocExtension):
    TreeProcessorClass = TocTreeprocessor


def makeExtension(**kwargs) -> TocExtension:
    return TocExtension(**kwargs)
