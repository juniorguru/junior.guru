import os
import re
import sys
from itertools import takewhile

from lxml import html


DEBUG = bool(os.getenv('DEBUG_SECTIONS_PARSER'))

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

BULLET_PATTERN = r'\W{1,2}'
MIN_LIST_ITEMS = 2

MULTIPLE_NEWLINES_RE = re.compile(r'\n{2,}')
WHITESPACE_RE = re.compile(r'\s+')
SENTENCE_END_RE = re.compile(r'([\?\.\!\:\;…]+ |\.\.\. |\n)')
BULLET_RE = re.compile(r'^' + BULLET_PATTERN + r'$')


class Pipeline():
    def process_item(self, item, spider):
        item['sections'] = [section.to_dict() for section
                            in parse_sections(item['description_html'])]
        return item


# Honestly, the tokens could have been dicts and the parser would still
# work the same, but having them as objects allows for somewhat easier
# debugging.


class Token():
    """Base token class just to please OOP gods"""
    pass


class TextFragment(Token):
    """Represents fragments of text which are yet to be parsed into sections"""

    def __init__(self, content):
        assert isinstance(content, str), 'Content must be string'
        self.content = content

    def __hash__(self):
        return hash(self.content)

    def __eq__(self, other):
        return other and self.content == other.content

    def __str__(self):
        return self.content

    def __repr__(self):
        return f"<TextFragment({repr(shorten_text(self.content))})>"


class BaseSection(Token):
    """
    Represents parsed sections

    The heading must be a string even if empty to avoid None floating
    randomly around.
    """

    def __init__(self, heading, contents):
        assert self.type, f"{self.__class__.__name__} doesn't have type set"
        assert isinstance(heading, str), 'Heading must be string'
        self.heading = heading
        assert isinstance(contents, list), 'Contents must be list'
        self.contents = contents

    def __hash__(self):
        return hash((self.heading, self.contents))

    def __eq__(self, other):
        return (other and
                self.heading == other.heading and
                self.contents == other.contents)

    def __repr__(self):
        cls_name = self.__class__.__name__
        if self.heading:
            heading = repr(shorten_text(self.heading))
            return f"<{cls_name}(heading={heading})>"
        try:
            first_sentence = repr(shorten_text(self.contents[0]))
        except IndexError:
            first_sentence = "''"
        return f"<{cls_name}(contents={first_sentence})>"

    def to_dict(self):
        data = dict(type=self.type, contents=self.contents)
        if self.heading:
            data['heading'] = self.heading
        return data


class ParagraphSection(BaseSection):
    """
    Represents parsed paragraph section

    Each item of the contents is a single "sentence" from the paragraph.
    """
    type = 'paragraph'


class ListSection(BaseSection):
    """
    Represents parsed list section

    Each item of the contents is a single bullet point from the list.
    """
    type = 'list'


# Parser functions! So parse_sections() is the mothership where everything
# happens, parse_html_list() takes care of extracting HTML lists, and
# parse_textual_lists() takes care of extracting textual lists (i.e. visual
# lists with manual bullet prefixes in front of each line).
#
# The rough idea here is that the parser takes a blob of text, identifies
# the list sections inside, then cuts the text into fragments at the exact
# places where the sections has been found, and then puts together the text
# fragments and sections in the right order.
#
# The HTML sections are identified first, as they're the easiest to spot
# and have a natural priority. Then the remaining text fragments are being
# searched for textual lists. After that, the remaining text fragments are
# turned into paragraph sections in which "sentences" are the contents.


def parse_sections(description_html):
    description_html = normalize_space(description_html)

    # parse HTML and pre-process it to clean up ugly cases
    html_tree = html.fromstring(description_html)
    for preprocess in [fix_orphan_html_list_items,
                       fix_disconnected_html_lists,
                       flatten_nested_html_lists]:
        html_tree = preprocess(html_tree)
        debug_el(f'PREPROCESS {preprocess.__name__.upper()}', html_tree)

    # identify HTML lists
    sections = parse_html_lists(html_tree)
    sections = debug_iter('HTML_LIST_SECTIONS', sections)

    # identify text fragments before, between, and after the lists we've
    # been able to parse, get a list of tokens as they go one after another
    text = extract_text(html_tree)
    tokens = split_by_sections(TextFragment(text), sections)
    tokens = debug_iter('TOKENS_AFTER_HTML_LISTS', tokens)

    # identify textual lists in each text fragment and get a list
    # of tokens as they go one after another
    def split_by_textual_list_sections(text_fragment):
        sections = parse_textual_lists(text_fragment.content)
        debug('split_by_textual_list_sections() TEXT_FRAGMENT', repr(text_fragment))
        sections = debug_iter('split_by_textual_list_sections() SECTIONS', sections)
        return split_by_sections(text_fragment, sections)

    tokens = process_text_fragments(tokens, split_by_textual_list_sections)
    tokens = debug_iter('TOKENS_AFTER_TEXTUAL_LISTS', tokens)

    # if still no sections found, try the bold/newline parser as last resort
    tokens = list(tokens)
    if len(tokens) == 1:
        token = tokens[0]
        if is_text_fragment(token):
            sections = parse_bold_nl_lists(html_tree, text)
            tokens = split_by_sections(token, sections)
            tokens = debug_iter('TOKENS_AFTER_BOLD_NL_LISTS', tokens)

    # turn the remaining text fragments into paragraphs
    tokens = process_text_fragments(tokens, to_paragraph_sections)
    tokens = debug_iter('TOKENS_AFTER_PARAGRAPHS', tokens)
    return tokens


def parse_html_lists(el):
    for list_el in el.cssselect('ul, ol'):
        # get first text before the list and pronounce it to be the list header
        heading = None
        for sibling_el in list_el.itersiblings(preceding=True):
            if sibling_el.tail:
                tail_text = normalize_space(sibling_el.tail)
                if tail_text:
                    heading = tail_text
                    break

            text = extract_text(sibling_el).split('\n')[-1]
            if text:
                heading = text
                break
        if not heading:
            for ancestor_el in list_el.iterancestors():
                if ancestor_el.text:
                    text = normalize_space(ancestor_el.text)
                    if text:
                        heading = text
                        break
        heading = heading or ''

        # pronounce text content of all the list items to be list items;
        # any tail texts are treated just as list items
        list_items = []
        for li_el in list_el.cssselect('li'):
            list_items.extend(extract_text(li_el).split('\n'))
            tail_text = normalize_space(li_el.tail) if li_el.tail else ''
            if tail_text:
                list_items.append(tail_text)

        yield ListSection(heading, list_items)


def parse_textual_lists(text):
    # iterate over lines, detect bullet characters (line prefix), and
    # construct lists with headings
    lines = [line.strip() for line in text.splitlines()]
    list_items = []
    previous_prefix = None

    for i, line in enumerate(lines):
        parts = WHITESPACE_RE.split(line, maxsplit=1)
        try:
            prefix, line_reminder = parts
        except ValueError:
            prefix, line_reminder = parts[0], ''

        if BULLET_RE.match(prefix) and prefix == previous_prefix:
            list_items.append(line_reminder)
        else:
            list_items_count = len(list_items)
            if list_items_count >= MIN_LIST_ITEMS:
                heading_i = i - list_items_count - 1
                heading = '' if heading_i < 0 else lines[heading_i]
                yield ListSection(heading, list_items)
            list_items = [line_reminder]

        previous_prefix = prefix

    list_items_count = len(list_items)
    if list_items_count >= MIN_LIST_ITEMS:
        heading_i = len(lines) - list_items_count - 1
        heading = '' if heading_i < 0 else lines[heading_i]
        yield ListSection(heading, list_items)


def parse_bold_nl_lists(el, text):
    headings = {extract_text(bold_el) for bold_el
                in el.cssselect('strong, b, u')}

    heading = None
    list_items = []
    for line in text.splitlines():
        if line in headings:
            if heading:
                if len(list_items) >= MIN_LIST_ITEMS:
                    yield ListSection(heading, list_items)
                list_items = []
            heading = line
        elif heading:
            list_items.append(line)

    if len(list_items) >= MIN_LIST_ITEMS:
        yield ListSection(heading, list_items)


# HTML pre-processors. They fix ugly HTML soap before any parsing happens.


def fix_orphan_html_list_items(el):
    while True:
        try:
            li_el = el.xpath('//li[not(parent::ul) and not(parent::ol)]')[0]
        except IndexError:
            break
        else:
            parent_el = li_el.getparent()
            i = parent_el.index(li_el)  # index of the first <li>
            subsequent_li_els = list(takewhile(is_li_element,
                                               li_el.itersiblings()))
            if subsequent_li_els:
                # prepare new children, the first <li> and all subsequent <li>
                # siblings (anything else than <li> is a stopper)
                children_els = [li_el] + subsequent_li_els

                # move <li> elements from the parent to the new <ul>
                ul_el = html.Element('ul')
                for child_el in children_els:
                    ul_el.append(child_el)

                # move tail text from the last <li> to the new <ul>
                ul_el.tail = children_els[-1].tail
                children_els[-1].tail = None

                # put the <ul> at the same index where the first <li> was
                parent_el.insert(i, ul_el)
            else:
                # standalone <li> element, turn it into a <span> with <br>
                br_el = html.Element('br')
                li_el.addnext(br_el)
                li_el.tag = 'span'
    return el


def is_li_element(el):
    return el.tag == 'li'


def fix_disconnected_html_lists(el):
    while True:
        stop = True
        for ul_li in el.xpath('//ul'):
            tail = (ul_li.tail or '').strip()
            next_el = ul_li.getnext()
            if not tail and next_el is not None and next_el.tag == 'ul':
                stop = False

                # move all children from the next <ul> to the current
                for child_el in next_el.getchildren():
                    ul_li.append(child_el)

                # move tail from the next <ul> to the current one
                ul_li.tail = next_el.tail

                # remove the next <ul>
                next_el.getparent().remove(next_el)
        if stop:
            break
    return el


def flatten_nested_html_lists(el):
    while True:
        try:
            inner_li_el = el.xpath('//li//li')[0]
        except IndexError:
            break
        else:
            inner_list_el = inner_li_el.getparent()
            inner_els = [inner_li_el] + list(inner_li_el.itersiblings())
            outter_li_el = next(inner_li_el.iterancestors(tag='li'))

            # move elements from the inner list to the outter
            last_el = outter_li_el
            for inner_el in inner_els:
                last_el.addnext(inner_el)
                last_el = inner_el

            # move tail text from the inner list to the last flattened <li>
            last_el.tail = inner_list_el.tail

            # clean up the inner container list
            inner_list_el.getparent().remove(inner_list_el)
    return el


# Helper functions! These do not carry the weight of parsing algorithms,
# they're the supporting crew.


def extract_text(el):
    """
    Removes HTML tags from given HTML node, normalizes whitespace with
    respect to how the HTML would been perceived if rendered, and returns text

    The text returned by this function can be assumed to:

    - Contain no HTML,
    - have all visual line breaks normalized as a single new line character,
    - have all other white space normalized as a single space character.
    """
    # iterate over all elements which visually imply line break when rendered
    # in the browser and add the line break explicitly to their tail
    for newline_el in el.cssselect(', '.join(NEWLINE_ELEMENT_NAMES)):
        tail_text = newline_el.tail
        newline_el.tail = f'\n\n{tail_text}' if tail_text else '\n\n'

    # serialize the html tree and remove tags, but keep all whitespace
    # as it was so we know where the visual line breaks are
    #
    # normalize space characters, because now HTML entities got decoded
    text = normalize_space(el.text_content())

    # turn the visual line breaks into new line characters, turn any
    # other space characters into a single space character
    return '\n'.join(split_blocks(text))


def is_text_fragment(token):
    return isinstance(token, TextFragment)


def process_text_fragments(tokens, fn):
    for token in tokens:
        if is_text_fragment(token):
            yield from fn(token)
        else:
            yield token


def split_by_sections(text_fragment, sections):
    tokens = [text_fragment]
    for section in sections:
        def split(text_fragment):
            return split_by_section(text_fragment, section)

        tokens = list(process_text_fragments(tokens, split))
        debug('split_by_sections() TEXT_FRAGMENT', repr(text_fragment))
        debug('split_by_sections() SECTION', section)
        debug_iter('split_by_sections() TOKENS', tokens)
    return tokens


def split_by_section(text_fragment, section):
    # create a regexp representing the section
    section_re = section_to_re(section)
    debug('split_by_section() TEXT_FRAGMENT_CONTENT', repr(text_fragment.content))
    debug('split_by_section() SECTION_RE', repr(section_re.pattern))

    # split the text by the regexp, create new text fragments, intersperse
    # the section in between the new text fragments
    text_fragments = [TextFragment(content.strip()) for content
                      in section_re.split(text_fragment.content)]
    debug('split_by_section() SPLIT_RESULTS_COUNT', len(text_fragments))
    tokens = intersperse(text_fragments, section)

    # skip text fragments with no content
    return (token for token in tokens
            if not is_text_fragment(token) or token.content)


def section_to_re(section):
    if not section.contents:
        raise ValueError(f"Section {repr(section)} doesn't have any contents")

    # optional bullet, marked as non-capturing by ?: so
    # the subsequent re.split() won't put the bullets into split results
    bullet_ptn = r'(?:' + BULLET_PATTERN + r' )?'
    contents_ptn = r'\s+'.join(bullet_ptn + re.escape(content)
                               for content in section.contents)

    if section.heading:
        heading_ptn = re.escape(section.heading)
        section_ptn_parts = [heading_ptn, contents_ptn]
    else:
        section_ptn_parts = [contents_ptn]

    return re.compile(r'\s*' + r'\s+'.join(section_ptn_parts) + r'\s*')


def intersperse(lst, item):
    """
    Puts the item in between each two items in the list

    Dark magic, but efficient. I think. I don't understand the code myself,
    I had to unit-test it to believe that it works the way I want!
    Copy-pasted from https://stackoverflow.com/a/5921708/325365
    """
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result


def to_paragraph_sections(text_fragment):
    yield ParagraphSection('', split_sentences(text_fragment.content))


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


def normalize_space(text):
    return text.translate(SPACE_TRANSLATION_TABLE).strip()


def shorten_text(text, max_chars=10):
    if len(text) < max_chars:
        return text
    return text[:10] + '…'


def debug(label, *args):
    if DEBUG:
        print(label, *args, file=sys.stderr)


def debug_el(label, el):
    if DEBUG:
        print(label, repr(html.tostring(el, encoding=str)), file=sys.stderr)


def debug_iter(label, iterable):
    if DEBUG:
        iterable = list(iterable)
        print(label, iterable, file=sys.stderr)
    return iterable
