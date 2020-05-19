import re


SENIOR_TITLE_RE = re.compile(r'\bsenior\b', re.IGNORECASE)
JUNIOR_TITLE_RE = re.compile(r'\bjunior\b', re.IGNORECASE)


class Pipeline():
    def process_item(self, item, spider):
        features = []
        features.extend(parse_from_title(item['title'], item['lang']))
        features.extend(parse_from_sentences(item['description_sentences'],
                                             item['lang']))
        item['features'] = features
        return item


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


def is_supressed(feature_id, sentence, suppressing_rules):
    for feature_id_matcher, rule_re in suppressing_rules:
        is_relevant_rule = (feature_id_matcher == '' or
                            feature_id_matcher == feature_id)
        if is_relevant_rule and rule_re.search(sentence):
            return True
    return False


def parse_from_sentences(sentences, lang):
    lang_suffix = lang.upper()
    feature_defs = GLOBALS[f'FEATURE_DEFS_{lang_suffix}']
    suppressing_rules = GLOBALS[f'SUPPRESSING_RULES_{lang_suffix}']

    for sentence in sentences:
        for feature_id, feature_re in feature_defs:
            if feature_re.search(sentence) and not is_supressed(feature_id, sentence, suppressing_rules):
                yield (feature_id, sentence, feature_re.pattern)


def parse_from_title(title, lang):
    is_senior_mentioned = SENIOR_TITLE_RE.search(title)
    is_junior_mentioned = JUNIOR_TITLE_RE.search(title)

    if is_senior_mentioned and not is_junior_mentioned:
        yield ('EXPLICITLY_SENIOR', title, None)
    elif is_junior_mentioned:
        yield ('EXPLICITLY_JUNIOR', title, None)
