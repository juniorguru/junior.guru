import re

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

MULTIPLE_NEWLINES_RE = re.compile(r'\n{2,}')
WHITESPACE_RE = re.compile(r'\s+')
SENTENCE_END_RE = re.compile(r'(?<!\bmin)([\?\.\!\:\;…]+ |\.\.\. |\n)')  # TODO more abbreviations?


class Pipeline():
    def process_item(self, item, spider):
        contents = parse_contents(item['description_raw'])
        item['contents'] = contents
        item['features'] = list(parse_features(contents, item['lang']))
        return item


def parse_contents(description_raw):
    return split_sentences(extract_text(description_raw))


def compile_rules(rules):
    return [(identifier, re.compile(''.join([
                '' if pattern[0] == '^' else r'\b',
                pattern,
                '' if pattern[-1] == '$' else r'\b',
            ]), re.IGNORECASE))
            for identifier, pattern in rules]


# TODO
# matching 'senior' in title (when there's no 'junior')
# plus points for 'junior' in title
# At least 5 years’ experience as an iOS mobile developer.
# Experience leading a team
# AJ minimálně na úrovni technické specifikace
# Angličtinu minimálně na úrovni technické specifikace
# Lead a growing team
# At least five years’ experience as a cloud engineer
# have Computing Degree
# Czech/Slovak language knowledge/possibly is essential
# execute tasks independently with little supervision and under pressure
# strong Java development background
# English language knowledge at least B1 technical level, very much welcome
# experienced Java developer
# Vzdělání:vyšší odborné, SŠ s maturitou, bakalářské, vysokoškolské
# Although team language is Czech - basic English knowledge is required
# Well-founded completed training in computer science / electrical engineering (HTL, FH or University)
# Two or more years of hands-on experience
# You have a degree in Computer Science, Mathematics, Physics or Business Administration.
# working experience in (software) development
# Excellent analytical and problem-solving skills
# Able to work with minimal supervision
# Advanced knowledge of written and spoken English
# BS or MS in software engineering or equivalent experience
# Solid technical background
# work independently
# (Proven )commercial experience working with Java
# sound knowledge of
# Good english communication skills
# Strong experience (5+ years) in
# previous experience in ???
# significant (technical) background
# English is required
# work autonomously
# very solid know-how
# take responsibility for good architecture and software design
# After your studies in mathematics, computer science, engineering, business or comparable studies
# you have gained professional experience
# Very good programming skills and practical experience
# state-of-the-art
# Completed technical education (college or university level)
# experience ... building ... complex
# SŠ/VŠ vzdělání technického zaměření
# Independent working ability
# Bachelor’s degree or higher (min A- average for under-graduate, first class for post-graduate).
# Independent, self-directing working style.
# experience as a Technical Leader
# leadership skills
# Leadership experience
# Znalost problematiky programování webových aplikací (min. 3 roky)

# !!!
# http://localhost:5000/admin/jobs-scraped/#7a081488f0f6b53d28c4bc4d8fc2801972bd5e21d9b5756fed9636f5
#
# 'Nice to Have',
# 'Completed studies in computer science',


# TODO density of words like experience/knowledge/zkušenosti/dobrá znalost/...


FEATURE_DEFS_EN = compile_rules([
    ('DEGREE_REQUIRED', r'degree in'),
    ('YEARS_EXPERIENCE_REQUIRED', r'[\d\-\+\s]+[^\d]+years?.? [\w\s]* experience'),
    ('ADVANCED_KNOWLEDGE_REQUIRED', r'deep familiarity'),
    ('ADVANCED_KNOWLEDGE_REQUIRED', r'(excellent|strong|very good) [\w\s]* (skills|abilities|capabilities|knowledge|experience)'),
    ('ADVANCED_KNOWLEDGE_REQUIRED', r'(commercial|solid|work) experience'),
    ('ADVANCED_KNOWLEDGE_REQUIRED', r'you are [\w\s]* experienced'),
    ('ADVANCED_KNOWLEDGE_REQUIRED', r'self-starter'),
    ('ADVANCED_KNOWLEDGE_REQUIRED', r'previous experience with'),
    ('ADVANCED_KNOWLEDGE_REQUIRED', r'leadership (experience|skills)'),
])
SUPPRESSING_RULES_EN = compile_rules([
    ('', r'(is|are) a (big )?plus'),
    ('', r'is [\w\s]* advantage'),
    ('ADVANCED_KNOWLEDGE_REQUIRED', r'communication skills'),
    ('ADVANCED_KNOWLEDGE_REQUIRED', r'english'),
])

FEATURE_DEFS_CS = compile_rules([
    ('ENGLISH_REQUIRED', r'angličtin\w+'),
    ('DEGREE_REQUIRED', r'vysokoškolské vzdělání'),
    ('ADVANCED_KNOWLEDGE_REQUIRED', r'velmi dobr\w+ znalost'),
    ('ADVANCED_KNOWLEDGE_REQUIRED', r'seniorní znalost'),
])
SUPPRESSING_RULES_CS = compile_rules([
    ('', r'výhodou'),
])

GLOBALS = globals()


def is_supressed(feature_id, content, suppressing_rules):
    for feature_id_matcher, rule_re in suppressing_rules:
        is_relevant_rule = (feature_id_matcher == '' or
                            feature_id_matcher == feature_id)
        if is_relevant_rule and rule_re.search(content):
            return True
    return False


def parse_features(contents, lang):
    lang_suffix = lang.upper()
    feature_defs = GLOBALS[f'FEATURE_DEFS_{lang_suffix}']
    suppressing_rules = GLOBALS[f'SUPPRESSING_RULES_{lang_suffix}']

    for content in contents:
        for feature_id, feature_re in feature_defs:
            if feature_re.search(content) and not is_supressed(feature_id, content, suppressing_rules):
                yield (feature_id, content, feature_re.pattern)


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
    #
    # normalize space characters, because now HTML entities got decoded
    text = normalize_space(el.text_content())

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
