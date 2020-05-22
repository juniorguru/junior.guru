import re


# TODO at the end the grades should normalize (highest within ad = 100%, lowest = 0%)


WEIGHT_IS_REQ = 4
WEIGHT_ISNT_REQ = -1 * WEIGHT_IS_REQ
WEIGHT_IS_REQ_MAYBE = 2
WEIGHT_ISNT_REQ_MAYBE = -1 * WEIGHT_IS_REQ_MAYBE


class Pipeline():
    def process_item(self, item, spider):
        item['jg_rank'] = calc_jg_rank(item['features'])
        return item


def calc_jg_rank(features, lang):
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
