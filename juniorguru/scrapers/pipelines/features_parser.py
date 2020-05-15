import re


WEIGHT_IS_REQ = 4
WEIGHT_ISNT_REQ = -1 * WEIGHT_IS_REQ
WEIGHT_IS_REQ_MAYBE = 2
WEIGHT_ISNT_REQ_MAYBE = -1 * WEIGHT_IS_REQ_MAYBE

RESEMBLES_HEADING_RE = re.compile(r':$')


def compile_res(*patterns):
    return [re.compile(r'\b(' + pattern + r')\b', re.IGNORECASE)
            for pattern in patterns]


HEADINGS_IS_REQ = {
    'en': compile_res(
        r'knowledge',
        r'experience',
        r'qualifications',
        r'education',
        r'required skills',
        r'skills required',
        r'hard skills',
        r'soft skills',
        r'key skills',
        r'must have',
        r'background',
        r'we need you to[\w\s]+have',
    ),
    'cs': compile_res(
        r'požadujeme',
        r'požadavky',
        r'očekáváme',
        r'znalosti',
        r'schopnosti',
    ),
}
HEADINGS_IS_REQ_MAYBE = {
    'en': compile_res(
        r'basics',
        r'profile',
        r'skills?',
        r'restrictions',
        r'features',
        r'looking for',
        r'see in you',
    ),
    'cs': compile_res(
        r'hledáme',
        r'pokud má(te|š)',
        r'splň(ovat|uješ|ujete)',
    ),
}
HEADINGS_ISNT_REQ = {
    'en': compile_res(
        r'additional',
        r'benefits',
        r'perks',
        r'responsibilities',
        r'area of responsibility',
        r'we offer',
        r'nice to have',
        r'we value',
        r'your role',
        r'role description',
        r'^role:?$',
        r'plus',
        r'not required',
        r'advantages?',
        r'package',
        r'technology stack',
        r'dev ?stack',
        r'tools we use',
        r'how we develop',
        r'secondary',
        r'mission',
        r'your tasks',
        r'optional',
        r'expect from us',
    ),
    'cs': compile_res(
        r'na čem[\w\s]+pracovat',
        r'náplň práce',
        r'nabídka',
        r'nabízíme',
        r'co děláme',
        r'kdo jsme',
        r'výhodou',
        r'těšit',
        r'mohlo[\w\s]+hodit',
        r'získá(š|te)',
        r'dev ?stack',
    ),
}


class Pipeline():
    def process_item(self, item, spider):
        item['features'] = list(parse_features(item['sections'], item['lang']))
        return item


def parse_features(sections, lang):
    # TODO if section contents grade high on the scale of the whole job ad, they should get extra MAYBE
    # TODO at the end the grades should normalize (highest within ad = 100%, lowest = 0%)
    # TODO top graded contents go right into requirements parser, which produces '_REQUIRED' features (LANG_EN_REQUIRED, UNIVERSITY_REQUIRED)
    # TODO all other content goes through other analysis, which produces PYTHON form cs ads, ...
    # TODO cs ad automatically produces LANG_CS_REQUIRED, en ad produces LANG_EN_REQUIRED
    # TODO the parse result is (feature_id, source_content)
    for section in sections:
        section_req_grade = calc_section_req_grade(section, lang)
        for content in section['contents']:
            content_req_grade = calc_content_req_grade(content, lang)
            yield (content, section_grade + content_req_grade)


def calc_section_req_grade(section, lang):
    grade = 0
    grade += one_or_zero(section['type'] == 'list') * WEIGHT_IS_MAYBE

    heading = section.get('heading')
    if heading:
        for is_re in HEADINGS_IS_REQ[lang]:
            grade += one_or_zero(is_re.search(heading)) * WEIGHT_IS_REQ
        for is_re in HEADINGS_IS_REQ_MAYBE[lang]:
            grade += one_or_zero(is_re.search(heading)) * WEIGHT_IS_REQ_MAYBE
        for is_re in HEADINGS_ISNT_REQ[lang]:
            grade += one_or_zero(is_re.search(heading)) * WEIGHT_ISNT_REQ

    return grade


def calc_content_req_grade(content, lang):
    return 0  # TODO


def one_or_zero(value):
    return 1 if value else 0
