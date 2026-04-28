import re

from markdownify import MarkdownConverter

from jg.coop.lib.text import normalize_space
from jg.coop.lib.youtube import parse_youtube_id


def truncate_discord_text(text: str, max_length: int, placeholder: str = "…") -> str:
    if len(text) <= max_length:
        return text

    if len(placeholder) >= max_length:
        return placeholder[:max_length]

    trimmed = text[: max_length - len(placeholder)].rstrip()
    return f"{trimmed}{placeholder}"


def _fix_whitespace(text: str, marker: str) -> str:
    """
    If the inline element's text ends with white space,
    put the markdown marker before the white space,
    so that the white space is treated correctly.
    """
    stripped_text = text.rstrip("\n")
    trailing_newlines = text[len(stripped_text) :]

    if not stripped_text:
        return trailing_newlines

    # avoid producing markdown like "**text **" when HTML carries
    # non-significant trailing spacing inside inline tags
    stripped_text = stripped_text.rstrip()

    if not stripped_text:
        return trailing_newlines

    return f"{marker}{stripped_text}{marker}{trailing_newlines}"


class DiscordMarkdownConverter(MarkdownConverter):
    class Options(MarkdownConverter.DefaultOptions):
        heading_style = "ATX"
        bullets = "-"
        strip = ["div"]
        wrap = False

    def convert_br(self, el, text, parent_tags) -> str:
        return "\n"

    def convert_strong(self, el, text, parent_tags) -> str:
        return _fix_whitespace(text, "**")

    def convert_b(self, el, text, parent_tags) -> str:
        return _fix_whitespace(text, "**")

    def convert_em(self, el, text, parent_tags) -> str:
        return _fix_whitespace(text, "*")

    def convert_i(self, el, text, parent_tags) -> str:
        return _fix_whitespace(text, "*")

    def convert_span(self, el, text, parent_tags) -> str:
        if not text.strip():
            return ""
        return text

    def convert_iframe(self, el, text, parent_tags) -> str:
        src = el.get("src") or ""
        try:
            if video_id := parse_youtube_id(src):
                return f"https://www.youtube.com/watch?v={video_id}"
        except ValueError:
            pass
        return ""


def to_discord_markdown(html: str) -> str:
    markdown = DiscordMarkdownConverter().convert(html)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return f"{normalize_space(markdown).strip()}\n"
