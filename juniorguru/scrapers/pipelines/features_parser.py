import re


MIN_SCORE = 0


def rc(pattern):
    return re.compile(pattern, re.IGNORECASE)


IS_TRUE_HEADING = rc(r':$')
IS_REQUIREMENTS_HEADINGS = {
    'en': [
        rc(r'knowledge'),
        rc(r'experience'),
        rc(r'qualifications'),
        rc(r'education'),
        rc(r'required skills'),
        rc(r'skills required'),
        rc(r'hard skills'),
        rc(r'soft skills'),
        rc(r'key skills'),
        rc(r'must have'),
        rc(r'background'),
        rc(r'we need you to[\w\s]+have'),
    ],
    'cs': [
        rc(r'požadujeme'),
        rc(r'požadavky'),
        rc(r'očekáváme'),
        rc(r'znalosti'),
        rc(r'schopnosti')
    ],
}
COULD_BE_REQUIREMENTS_HEADINGS = {
    'en': [
        rc(r'basics'),
        rc(r'profile'),
        rc(r'skills?'),
        rc(r'restrictions'),
        rc(r'features'),
        rc(r'looking for'),
        rc(r'see in you'),
    ],
    'cs': [
        rc(r'hledáme'),
        rc(r'pokud má(te|š)'),
        rc(r'splň(ovat|uješ|ujete)'),
    ],
}
ISNT_REQUIREMENTS_HEADINGS = {
    'en': [
        rc(r'additional'),
        rc(r'benefits'),
        rc(r'perks'),
        rc(r'responsibilities'),
        rc(r'area of responsibility'),
        rc(r'we offer'),
        rc(r'nice to have'),
        rc(r'we value'),
        rc(r'your role'),
        rc(r'role description'),
        rc(r'^role:?$'),
        rc(r'plus'),
        rc(r'not required'),
        rc(r'advantages?'),
        rc(r'package'),
        rc(r'technology stack'),
        rc(r'dev ?stack'),
        rc(r'tools we use'),
        rc(r'how we develop'),
        rc(r'secondary'),
        rc(r'mission'),
        rc(r'your tasks'),
        rc(r'optional'),
        rc(r'expect from us'),
    ],
    'cs': [
        rc(r'na čem[\w\s]+pracovat'),
        rc(r'náplň práce'),
        rc(r'nabídka'),
        rc(r'nabízíme'),
        rc(r'co děláme'),
        rc(r'kdo jsme'),
        rc(r'výhodou'),
        rc(r'těšit'),
        rc(r'mohlo[\w\s]+hodit'),
        rc(r'získá(š|te)'),
        rc(r'dev ?stack'),
    ],
}
TYPICAL_REQUIREMENTS_CONTENTS = {
    'en': [
        rc(r''),
    ],
    'cs': [
        rc(r''),
    ],
}


class Pipeline():
    def process_item(self, item, spider):
        item['features'] = list(parse_features(item['sections']))
        return item


def parse_features(sections):
    all_headers = {section['header'] for section in sections
                   if section.get('header')}
    for section in sections:
        other_headers = all_headers - {section.get('header')}
        score = calc_section_score(section, other_headers)
        if score >= MIN_SCORE:
            yield from ((c, score) for c in section['contents'])


def calc_section_score(section, other_headers):
    header_score = 0
    contents_score = 0
    return header_score + contents_score
