import re
import unicodedata

from lxml import html


# http://jkorpela.fi/chars/spaces.html
SPACE_TRANSLATION_TABLE = str.maketrans({
    '\u0020': ' ',  # SPACE
    '\u00a0': ' ',  # NO-BREAK SPACE
    '\u1680': '-',  # OGHAM SPACE MARK
    '\u180e': ' ',  # MONGOLIAN VOWEL SEPARATOR
    '\u2000': ' ',  # EN QUAD
    '\u2001': ' ',  # EM QUAD
    '\u2002': ' ',  # EN SPACE (nut)
    '\u2003': ' ',  # EM SPACE (mutton)
    '\u2004': ' ',  # THREE-PER-EM SPACE (thick space)
    '\u2005': ' ',  # FOUR-PER-EM SPACE (mid space)
    '\u2006': ' ',  # SIX-PER-EM SPACE
    '\u2007': ' ',  # FIGURE SPACE
    '\u2008': ' ',  # PUNCTUATION SPACE
    '\u2009': ' ',  # THIN SPACE
    '\u200a': ' ',  # HAIR SPACE
    '\u200b': None,  # ZERO WIDTH SPACE
    '\u202f': ' ',  # NARROW NO-BREAK SPACE
    '\u205f': ' ',  # MEDIUM MATHEMATICAL SPACE
    '\u3000': ' ',  # IDEOGRAPHIC SPACE
    '\ufeff': None,  # ZERO WIDTH NO-BREAK SPACE
})

# https://developer.mozilla.org/en-US/docs/Web/HTML/Block-level_elements#Elements
BLOCK_ELEMENT_NAMES = [
    'address', 'article', 'aside', 'blockquote', 'details', 'dialog',
    'dd', 'div', 'dl', 'dt', 'fieldset', 'figcaption', 'figure', 'footer',
    'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hgroup', 'hr',
    'li', 'main', 'nav', 'ol', 'p', 'pre', 'section', 'table', 'ul',
]
NEWLINE_ELEMENT_NAMES = BLOCK_ELEMENT_NAMES + ['br']

WHITESPACE_RE = re.compile(r'\s+')
MULTIPLE_NEWLINES_RE = re.compile(r'\n{2,}')

# TODO add support for more abbreviations
SENTENCE_END_RE = re.compile(r'''
    (?<!\b(                 # must not be preceeded by the following abbreviations
        min
    ))
    (
        [\?\.\!\:\;…]+\ |   # common "end of sentence" chars followed by a space
        \.\.\.\ |           # literal form of … followed by a space
        \n                  # new line
    )
''', re.VERBOSE)


class Pipeline():
    def process_item(self, item, spider):
        if item.get('description_html'):  # this line added for Mila and ML experiements
            description_text = extract_text(item['description_html'])
            item['description_text'] = description_text
            item['description_sentences'] = split_sentences(description_text)
            # TODO item['description_words'] = split_words(description_text, item['lang'])
        return item


def extract_text(html_text):
    """
    Removes HTML tags from given HTML, normalizes whitespace with
    respect to how the HTML would been perceived if rendered, and returns text

    The text returned by this function can be assumed to:

    - Contain no HTML,
    - have all visual line breaks normalized as a single new line character,
    - have all other white space normalized as a single space character.
    """
    el = html.fromstring(html_text)

    # iterate over all elements which visually imply line break when rendered
    # in the browser and add the line break explicitly to their tail
    for newline_el in el.cssselect(', '.join(NEWLINE_ELEMENT_NAMES)):
        tail_text = newline_el.tail
        newline_el.tail = f'\n\n{tail_text}' if tail_text else '\n\n'

    # serialize the html tree and remove tags, but keep all whitespace
    # as it was so we know where the visual line breaks are
    text = el.text_content()

    # now HTML entities got decoded, so normalize unicode
    # https://twitter.com/python_tip/status/1262725016153661440
    # and then normalize space characters
    text = normalize_space(unicodedata.normalize('NFC', text))

    # turn the visual line breaks into new line characters, turn any
    # other space characters into a single space character
    return '\n'.join(split_blocks(text))


def normalize_space(text):
    return text.translate(SPACE_TRANSLATION_TABLE).strip()


def split_blocks(text):
    """
    Split the text into blocks at the places of visual line breaks,
    and normalize any other white space chars as single space chars
    """
    blocks = (WHITESPACE_RE.sub(' ', block).strip()
              for block in MULTIPLE_NEWLINES_RE.split(text))
    return [block for block in blocks if block]


def split_sentences(text):
    """
    Splits given text into "sentences"

    The sentences are just approximate, there is no guarantee on correctness
    and there is no rocket science. The input text is assumed to have
    the guarantees provided by the extract_text() function.
    """
    return split_blocks(SENTENCE_END_RE.sub(r'\1\n\n', text))
