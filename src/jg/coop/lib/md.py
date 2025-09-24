import re

from markdown import markdown
from markdown.extensions.toc import TocExtension

from jg.coop.lib.text import extract_text


LINK_RE = re.compile(
    r"""
        \!?
        \[
            ([^\]]+)
        \]
        \(
            [^\)]+
        \)
    """,
    re.VERBOSE,
)

URL_RE = re.compile(r"https?://(www\.)?")


def md(markdown_text: str) -> str:
    return markdown(
        markdown_text,
        output_format="html5",
        extensions=[TocExtension(marker="", baselevel=1)],
    )


def strip_links(markdown_text: str) -> str:
    return LINK_RE.sub(r"\1", markdown_text)


def neutralize_urls(markdown_text: str) -> str:
    return URL_RE.sub("", markdown_text)


def md_as_text(markdown_text: str, newline: str = "\n") -> str:
    return extract_text(md(markdown_text), newline=newline)
