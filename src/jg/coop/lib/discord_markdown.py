from markdownify import markdownify


def to_discord_markdown(html: str) -> str:
    markdown = markdownify(html, heading_style="ATX", bullets="-", strip=["div"])
    return f"{markdown}\n"
