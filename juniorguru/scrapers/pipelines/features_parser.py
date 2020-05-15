import re


WEIGHT_IS_REQ = 4
WEIGHT_ISNT_REQ = -1 * WEIGHT_IS_REQ
WEIGHT_IS_REQ_MAYBE = 2
WEIGHT_ISNT_REQ_MAYBE = -1 * WEIGHT_IS_REQ_MAYBE

RESEMBLES_HEADING_RE = re.compile(r':$')


def hints(*patterns):
    return [re.compile(''.join([
                '' if pattern[0] == '^' else r'\b',
                pattern,
                '' if pattern[-1] == '$' else r'\b',
            ]), re.IGNORECASE) for pattern in patterns]


HEADINGS_IS_REQ = {
    'en': hints(
        r'knowledge',
        r'experience',
        r'qualifications',
        r'education',
        r'required skills',
        r'skills required',
        r'(hard|soft|key) skills',
        r'must have',
        r'background',
        r'we need you to[\w\s]+have',
    ),
    'cs': hints(
        r'požadujeme',
        r'požadavky',
        r'očekáváme',
        r'znalosti',
        r'schopnosti',
    ),
}
HEADINGS_IS_REQ_MAYBE = {
    'en': hints(
        r'basics',
        r'profile',
        r'skills?',
        r'restrictions',
        r'features',
        r'looking for',
        r'see in you',
    ),
    'cs': hints(
        r'hledáme',
        r'pokud má(te|š)',
        r'splň(ovat|uješ|ujete)',
    ),
}
HEADINGS_ISNT_REQ = {
    'en': hints(
        r'benefits',
        r'perks',
        r'responsibilities',
        r'area of responsibility',
        r'we offer',
        r'^we value:?$',
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
    'cs': hints(
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


CONTENT_IS_REQ = {
    'en': hints(
        r'years[\w\s]+of[\w\s]+experience',
        r'[\d+\s\-\+]+years?',
        r'familiar(ity)? with',
        r'skills',
        r'experience',
        r'knowledge of',
        r'at least',
        r'ability to',
        r'require[sd]',
        r'computer science',
        r'university',
        r'degree',
        r'understanding of',
        r'passion\w+ (for|about)',
        r'background',
        r'proficien(t|cy)',
        r'fluen(t|cy)',
        r'exposure (with|to)',
        r'or higher',
        r'is a must',
    ),
    'cs': hints(
        r'znalost\w*',
        r'vzdělání',
        r'prax[ei] v',
        r'zkušenost\w* se?',
        r'minimáln\w*',
        r'schopnost\w*',
        r'alespoň',
        r'profesionální úroveň',
        r'předchozí zkušenosti?',
        r'plynul\w+',
        r'požadujeme|požadován\w+',
        r'vědomosti',
        r'umíš|umíte|umět',
    ),
}
CONTENT_IS_REQ_MAYBE = {
    'en': hints(
        r'excellent',
        r'deep',
        r'strong',
        r'good',
        r'proven',
        r'basic',
        r'ideally',
        r'solid',
        r'extensive',
        r'desire',
    ),
    'cs': hints(
        r'dobr\w+',
        r'skvěl\w+',
        r'základ\w*',
        r'technologi\w+',
    ),
}
CONTENT_ISNT_REQ = {
    'en': hints(
        r'(is|are) a (big )?plus',
        r'is[\w\s]+advantage'
    ),
    'cs': hints(
        r'výhodou',
        r'vítány?|vítáme',
        r'ne( však)? podmínk\w+',
    ),
}


class Pipeline():
    def process_item(self, item, spider):
        item['features'] = list(parse_features(item['sections'], item['lang']))
        return item


def parse_features(sections, lang):
    # TODO choosing section with requirements if there are sections, otherwise analyzing all lines as requirements, multiplying by score?
    # TODO if section contents grade high on the scale of the whole job ad, they should get extra MAYBE
    # TODO at the end the grades should normalize (highest within ad = 100%, lowest = 0%)
    # TODO top graded contents go right into requirements parser, which produces '_REQUIRED' features (LANG_EN_REQUIRED, LANG_CS_REQUIRED, UNIVERSITY_REQUIRED)
    # TODO all other content goes through other analysis, which produces PYTHON form cs ads, ...
    # TODO cs ad automatically produces LANG_CS_REQUIRED, en ad produces LANG_EN_REQUIRED
    # TODO the parse result is (feature_id, source_content)

    # for section in sections:
    #     section_req_grade = calc_section_req_grade(section, lang)
    #     for content in section['contents']:
    #         content_req_grade = calc_content_req_grade(content, lang)
    #         yield (content, section_req_grade + content_req_grade)
    return []


def calc_section_req_grade(section, lang):
    grade = 0
    grade += one_or_zero(section['type'] == 'list') * WEIGHT_IS_REQ_MAYBE

    heading = section.get('heading')
    if heading:
        for hint_re in HEADINGS_IS_REQ[lang]:
            grade += one_or_zero(hint_re.search(heading)) * WEIGHT_IS_REQ
        for hint_re in HEADINGS_IS_REQ_MAYBE[lang]:
            grade += one_or_zero(hint_re.search(heading)) * WEIGHT_IS_REQ_MAYBE
        for hint_re in HEADINGS_ISNT_REQ[lang]:
            grade += one_or_zero(hint_re.search(heading)) * WEIGHT_ISNT_REQ

    return grade


def calc_content_req_grade(content, lang):
    grade = 0

    for hint_re in CONTENT_ISNT_REQ[lang]:
        return WEIGHT_ISNT_REQ

    for hint_re in CONTENT_IS_REQ[lang]:
        grade += one_or_zero(hint_re.search(heading)) * WEIGHT_IS_REQ
    for hint_re in CONTENT_IS_REQ_MAYBE[lang]:
        grade += one_or_zero(hint_re.search(heading)) * WEIGHT_IS_REQ_MAYBE

    return grade


def one_or_zero(value):
    return 1 if value else 0
