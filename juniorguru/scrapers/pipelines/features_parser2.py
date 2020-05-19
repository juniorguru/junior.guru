import itertools
import re


SENIOR_TITLE_RE = re.compile(r'\b(senior|seniorní|practiced)\b', re.IGNORECASE)
JUNIOR_TITLE_RE = re.compile(r'\b(junior|jnr|juniorní)\b', re.IGNORECASE)


def compile_rules(rules):
    return [(identifier, re.compile(''.join([
                '' if pattern[0] == '^' else r'\b',
                pattern,
                '' if pattern[-1] == '$' else r'\b',
            ]), re.IGNORECASE))
            for identifier, pattern in rules]


FEATURE_DEFS_EN = compile_rules([
    ('DEGREE_REQUIRED', r'degree in'),
    ('DEGREE_REQUIRED', r'(bachelor|university|graduate)'),
    ('DEGREE_REQUIRED', r'have\b.*\bdegree'),
    ('DEGREE_REQUIRED', r'studies\b.*\bin'),
    ('YEARS_EXPERIENCE_REQUIRED', r'[\d\-\+ ]+[^\d]+years?.?\b.*\bexperience'),
    ('YEARS_EXPERIENCE_REQUIRED', r'[\d\+ ]+experience'),
    ('ADVANCED_REQUIRED', r'deep familiarity'),
    ('ADVANCED_REQUIRED', r'(excellent|professional|strong|very good|thorough|solid|sound|significant)\b.*\b(skills|abilities|capabilities|knowledge|experience|background|understanding|know\-how|knowhow)'),
    ('ADVANCED_REQUIRED', r'(commercial|solid|work|working|previous) experience'),
    ('ADVANCED_REQUIRED', r'experience\b.*\b(architecting|building)'),
    ('ADVANCED_REQUIRED', r'responsibility\b.*\bfor\b.*\b(architecture|design)'),
    ('ADVANCED_REQUIRED', r'you are\b.*\bexperienced'),
    ('ADVANCED_REQUIRED', r'(seasoned|experienced|practiced)\b.*\b(developer|engineer)'),
    ('ADVANCED_REQUIRED', r'self-starter'),
    ('ADVANCED_REQUIRED', r'take responsibility'),
    ('ADVANCED_REQUIRED', r'previous experience with'),
    ('LEADERSHIP_REQUIRED', r'leadership (experience|skills)'),
    ('LEADERSHIP_REQUIRED', r'experience\b.*\b(leading|leader)'),
    ('LEADERSHIP_REQUIRED', r'lead(ing)?\b.*\bteams?'),
    ('CZECH_REQUIRED', r'czech\b.*\b(language|knowledge)'),
    ('SLOVAK_REQUIRED', r'slovak\b.*\b(language|knowledge)'),
    ('INDEPENDENCE_REQUIRED', r'(execute|work|working)\b.*\b(independently|autonomously)'),
    ('INDEPENDENCE_REQUIRED', r'(independent|autonomous)\b.*\bworking'),
    ('INDEPENDENCE_REQUIRED', r'(little|minimal|minimum) supervision'),
])
SUPPRESSING_RULES_EN = compile_rules([
    ('', r'(is|are) a (big )?plus'),
    ('', r'is\b.*\badvantage'),
    ('ADVANCED_REQUIRED', r'communication skills'),
    ('ADVANCED_REQUIRED', r'english'),
])

FEATURE_DEFS_CS = compile_rules([
    ('ENGLISH_REQUIRED', r'angličtin\w+'),
    ('DEGREE_REQUIRED', r'vysokoškolské vzdělání'),
    ('ADVANCED_REQUIRED', r'velmi dobr\w+ znalost'),
    ('ADVANCED_REQUIRED', r'seniorní znalost'),
])
SUPPRESSING_RULES_CS = compile_rules([
    ('', r'výhodou'),
])

FEATURE_DEFS = {'en': FEATURE_DEFS_EN, 'cs': FEATURE_DEFS_CS}
SUPPRESSING_RULES = {'en': SUPPRESSING_RULES_EN, 'cs': SUPPRESSING_RULES_CS}


class Pipeline():
    def process_item(self, item, spider):
        features = []
        features.extend(parse_from_title(item['title']))
        features.extend(parse_from_sentences(item['description_sentences'],
                                             item['lang']))
        item['features'] = features
        return item


def parse_from_title(title):
    senior_match = SENIOR_TITLE_RE.search(title)
    junior_match = JUNIOR_TITLE_RE.search(title)

    if senior_match and not junior_match:
        yield ('EXPLICITLY_SENIOR', senior_match.group(0),
               SENIOR_TITLE_RE.pattern)
    elif junior_match:
        yield ('EXPLICITLY_JUNIOR', junior_match.group(0),
               JUNIOR_TITLE_RE.pattern)


def parse_from_sentences(sentences, lang):
    return itertools.chain.from_iterable(parse_from_sentence(sentence, lang)
                                         for sentence in sentences)


def parse_from_sentence(sentence, lang):
    for feature_id, feature_re in FEATURE_DEFS[lang]:
        if (feature_re.search(sentence) and
            not is_supressed(feature_id, sentence, SUPPRESSING_RULES[lang])):
            yield (feature_id, sentence, feature_re.pattern)


def is_supressed(feature_id, sentence, suppressing_rules):
    for feature_id_matcher, rule_re in suppressing_rules:
        is_relevant_rule = (feature_id_matcher == '' or
                            feature_id_matcher == feature_id)
        if is_relevant_rule and rule_re.search(sentence):
            return True
    return False
