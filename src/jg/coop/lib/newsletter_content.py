import re
from dataclasses import dataclass

from lxml import html

from jg.coop.lib.md import md
from jg.coop.lib.reading_time import reading_time
from jg.coop.lib.template_filters import nplurals
from jg.coop.lib.text import extract_text, remove_emoji


MEETUPS_HEADING = "Srazy, konference a jiné akce"

STORIES_HEADING = "Nepřibarvené příběhy juniorů"

RECORDINGS_HEADING = "Záznamy z online akcí"

STORIES_URL_PREFIX = "junior.guru/stories/"

EVENTS_URL_PREFIX = "junior.guru/events/"

SUBJECT_PERIOD_RE = re.compile(r"^(\w+ \d{4}) ")

ITEM_RE = re.compile(r"^▪\ufe0f? (?P<text>.+) –$")

RECORDING_RE = re.compile(r"^(?P<speaker>[^:]+): (?P<title>.+)$")


@dataclass(frozen=True)
class NewsletterContent:
    html: str
    reading_time: int
    meetups_count: int
    story_headline: str
    recording_title: str

    def get_description(self, subject: str) -> str:
        if not (match := SUBJECT_PERIOD_RE.match(subject)):
            raise ValueError(f"Unexpected newsletter subject: {subject!r}")
        period = match.group(1).lower()
        meetups = (
            f"{self.meetups_count} "
            f"{nplurals(self.meetups_count, 'akce', 'akce', 'akcí')}"
        )
        return (
            f"Shrnutí pro juniory v IT za {period}: "
            f"{meetups} kam přijít, "
            f"příběh „{self.story_headline}“, "
            f"záznam z akce „{self.recording_title}“"
        )


def parse_newsletter(body: str) -> NewsletterContent:
    content_html = content_to_html(body)
    edited_html = edit_content_html(content_html)
    return NewsletterContent(
        html=edited_html,
        reading_time=reading_time(len(extract_text(content_html))),
        meetups_count=get_meetups_count(edited_html),
        story_headline=get_story_headline(edited_html),
        recording_title=get_recording_title(edited_html),
    )


def content_to_html(content_raw: str) -> str:
    """
    Detects if it's Markdown or HTML. Markdown can contain tags,
    so we need a heuristic. If the text contains Markdown links,
    it's probably Markdown.
    """
    if re.search(r"\[.*?\]\(.*?\)", content_raw):
        return md(content_raw)
    return content_raw


def edit_content_html(content_html: str) -> str:
    # remove double <br>
    content_html = re.sub(r"<br>\s*<br>", "<br>", content_html)

    # strip emoji from <h2> and <h3>
    content_html = re.sub(r"(<h2[^>]*>)(.*?)(</h2>)", _strip_emoji, content_html)
    content_html = re.sub(r"(<h3[^>]*>)(.*?)(</h3>)", _strip_emoji, content_html)

    # add trailing slash to course provider URLs to avoid redirects
    content_html = re.sub(
        r'(href="https://junior\.guru/courses/[\w-]+)(?=["?#])', r"\1/", content_html
    )

    return content_html


def get_meetups_count(content_html: str, heading: str = MEETUPS_HEADING) -> int:
    paragraphs = [
        el
        for el in get_section(content_html, heading)
        if el.tag == "p"
        and not (el.text or "").strip()
        and el[:1]
        and el[0].tag == "strong"
    ]
    if not paragraphs:
        raise ValueError(f"No meetups in the {heading!r} section")
    return len(paragraphs)


def get_story_headline(
    content_html: str,
    heading: str = STORIES_HEADING,
    url_prefix: str = STORIES_URL_PREFIX,
) -> str:
    return get_linked_item_text(content_html, heading, url_prefix)


def get_recording_title(
    content_html: str,
    heading: str = RECORDINGS_HEADING,
    url_prefix: str = EVENTS_URL_PREFIX,
) -> str:
    text = get_linked_item_text(content_html, heading, url_prefix)
    if match := RECORDING_RE.match(text):
        return match.group("title")
    raise ValueError(f"No speaker and title in {text!r}")


def get_linked_item_text(content_html: str, heading: str, url_prefix: str) -> str:
    """
    Returns text of the first list item linking to the given URL prefix,
    where items are lines like '▪️ Text – <a href="...">Link</a><br>'
    """
    for el in get_section(content_html, heading):
        for link in el.cssselect(f'a[href*="{url_prefix}"]'):
            line = " ".join(get_line_before(link).split())
            if match := ITEM_RE.match(line):
                return match.group("text")
            raise ValueError(f"Unexpected item {line!r} in the {heading!r} section")
    raise ValueError(f"No {url_prefix!r} link in the {heading!r} section")


def get_line_before(el: html.HtmlElement) -> str:
    parent = el.getparent()
    text = parent.text or ""
    for sibling in parent:
        if sibling is el:
            return text
        if sibling.tag == "br":
            text = sibling.tail or ""
        else:
            text += sibling.text_content() + (sibling.tail or "")
    raise ValueError("Element not found in its parent")


def get_section(content_html: str, heading: str) -> list[html.HtmlElement]:
    root = html.fragment_fromstring(content_html, create_parent="div")
    for h2 in root.cssselect("h2"):
        if h2.text_content().strip() == heading:
            section = []
            for el in h2.itersiblings():
                if el.tag == "h2":
                    break
                section.append(el)
            return section
    raise ValueError(f"Section {heading!r} not found in the newsletter issue")


def _strip_emoji(match: re.Match) -> str:
    return f"{match.group(1)}{remove_emoji(match.group(2))}{match.group(3)}"
