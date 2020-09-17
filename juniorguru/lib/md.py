from markdown import markdown
from markdown.extensions.toc import TocExtension


def md(markdown_text, heading_level_base=1):
    toc = TocExtension(marker='', baselevel=heading_level_base)
    return markdown(markdown_text, output_format='html5', extensions=[toc])
