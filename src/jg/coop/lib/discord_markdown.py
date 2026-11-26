import re
from datetime import UTC, datetime

from markdown import markdown
from markdownify import MarkdownConverter

from jg.coop.lib.text import normalize_space
from jg.coop.lib.youtube import parse_youtube_id


DISCORD_USER_MENTION_RE = re.compile(r"<@!?\d+>")

DISCORD_ROLE_MENTION_RE = re.compile(r"<@&\d+>")

DISCORD_CHANNEL_MENTION_RE = re.compile(r"<#\d+>")

DISCORD_CUSTOM_EMOJI_RE = re.compile(r"<a?:\w+:\d+>")

DISCORD_TIMESTAMP_RE = re.compile(r"<t:(-?\d+)(?::\w)?>")

DISCORD_SUPPRESSED_URL_RE = re.compile(r"<(https?://[^\s>]+)>")

DISCORD_SUBTEXT_RE = re.compile(r"^-# ", re.MULTILINE)

BARE_URL_RE = re.compile(r"(?<![(<\[])\bhttps?://[^\s<>()\[\]]+[^\s<>()\[\].,;:!?]")

LIST_ITEM = r"[ \t]*(?:[-*+]|\d+\.)[ \t]"

LIST_START_RE = re.compile(rf"^((?!{LIST_ITEM}).*\S.*)\n(?={LIST_ITEM})", re.MULTILINE)

HTML_HEADINGS_BASELEVEL = 4


def truncate_discord_markdown(
    text: str, max_length: int, placeholder: str = "…"
) -> str:
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


def discord_markdown_to_html(text: str) -> str:
    """
    Converts Discord message content to HTML for the web

    Mentions, custom emoji and timestamps make sense only inside Discord,
    so they're replaced with plain text. Any raw HTML is escaped.
    """
    text = DISCORD_USER_MENTION_RE.sub("@někdo", text)
    text = DISCORD_ROLE_MENTION_RE.sub("@role", text)
    text = DISCORD_CHANNEL_MENTION_RE.sub("#kanál", text)
    text = DISCORD_CUSTOM_EMOJI_RE.sub("", text)
    text = DISCORD_TIMESTAMP_RE.sub(_format_timestamp, text)
    text = DISCORD_SUPPRESSED_URL_RE.sub(r"\1", text)
    text = DISCORD_SUBTEXT_RE.sub("", text)
    text = text.replace("<", "&lt;")
    text = BARE_URL_RE.sub(r"<\g<0>>", text)
    text = LIST_START_RE.sub(r"\1\n\n", text)
    return markdown(
        text,
        output_format="html5",
        extensions=["nl2br", "sane_lists", "toc"],
        extension_configs={"toc": {"marker": "", "baselevel": HTML_HEADINGS_BASELEVEL}},
    ).strip()


def _format_timestamp(match: re.Match) -> str:
    timestamp = datetime.fromtimestamp(int(match.group(1)), UTC)
    return f"{timestamp.day}. {timestamp.month}. {timestamp.year}"
