import itertools
import re


LANG_MAPPING = {
    'en': 'ENGLISH_REQUIRED',
    'cs': 'CZECH_REQUIRED',
    'sk': 'SLOVAK_REQUIRED',
}

# [\b\W] is necessary because if the first thing ends with \W (e.g. period),
# the subseqent character doesn't qualify as a word boundary, also words
# followed by e.g. / wouldn't match
FOLLOWED_BY_PATTERN = r'[\b\W](.+[\b\W])?'


def rule(identifier, pattern, ignorecase=True):
    compile_flags = re.IGNORECASE if ignorecase else 0
    rule_re = re.compile(''.join([
        '' if pattern[0] == '^' else r'\b',  # implicit word boundary if not ^
        pattern,
        '' if pattern[-1] == '$' else r'\b',  # implicit word boundary if not $
    ]), compile_flags)
    return (identifier, rule_re)


def rules(identifier, patterns1, patterns2, **kwargs):
    patterns = itertools.product(patterns1, patterns2)
    try:
        if kwargs.pop('any_order'):
            patterns = itertools.chain(patterns,
                                       itertools.product(patterns2, patterns1))
    except KeyError:
        pass
    return [rule(identifier, FOLLOWED_BY_PATTERN.join(patterns), **kwargs)
            for patterns in patterns]


TECH_DEGREES_EN = [r'ph\.?d\.?', r'm\.?sc?\.?', r'b\.?sc?\.?',
                   r'bachelor[^ ]*s?', r'master[^ ]*s']
TECH_DEGREE_FIELDS_EN = [r'computer science', r'informatics', r'it',
                         r'software', r'technical', r'engineering', r'computing']
ADVANCED_SKILLS_ADJECTIVES_EN = [r'excellent', r'professional', r'strong',
                                 r'very good', r'thorough', r'solid', r'sound',
                                 r'significant', r'deep(er)?', r'extensive',
                                 r'superior', r'advanced', r'profound',
                                 r'detailed']
SKILLS_NOUNS_EN = [r'skills', r'abilities', r'capabilities', r'knowledge',
                   r'experience', r'background', r'understanding', r'expertise',
                   r'know.?how', r'familiarity']
LANGUAGE_KEYWORDS_EN = [r'language', r'knowledge', r'speak\w+', r'skills?',
                        r'native', r'command of', r'spoken', r'proficie\w+',
                        r'fluen\w+']


RULES_EN = (
    rules('TECH_DEGREE_REQUIRED',
          TECH_DEGREES_EN + [r'completed\b.*\beducation', r'degree', r'studies'],
          TECH_DEGREE_FIELDS_EN) +
    rules('TECH_DEGREE_REQUIRED',
          TECH_DEGREE_FIELDS_EN,
          [r'degree', r'education', r'university']) +
    rules('TECH_DEGREE_REQUIRED',
          TECH_DEGREES_EN,
          [r'degree', r'or higher']) +
    rules('ADVANCED_REQUIRED',
          ADVANCED_SKILLS_ADJECTIVES_EN,
          SKILLS_NOUNS_EN) +
    rules('ADVANCED_REQUIRED',
          [r'commercial', r'solid', r'work', r'working', r'previous', r'implementation', r'hands-on', r'architect\w+'],
          [r'experience', r'knowledge']) +
    rules('ADVANCED_REQUIRED',
          [r'experience'],
          [r'architect\w+', r'building', r'consuming', r'deploy\w+']) +
    rules('EXPLICITLY_SENIOR',
          [r'seasoned', r'experienced', r'practiced'],
          [r'engineer', r'developer']) +
    rules('CZECH_REQUIRED', [r'czech'], LANGUAGE_KEYWORDS_EN, any_order=True) +
    rules('SLOVAK_REQUIRED', [r'slovak'], LANGUAGE_KEYWORDS_EN, any_order=True) +
    rules('GERMAN_REQUIRED', [r'german'], LANGUAGE_KEYWORDS_EN, any_order=True)
) + [
    rule('TECH_DEGREE_REQUIRED', r'academic record'),
    rule('YEARS_EXPERIENCE_REQUIRED', r'[\d\-\+ ]+[^\d]+years?.?[\b ].*\b(experience|track record)'),
    rule('YEARS_EXPERIENCE_REQUIRED', r'experience\b.*[\d\-\+ ]+[^\d]+years?.?'),
    rule('YEARS_EXPERIENCE_REQUIRED', r'[\d\+] experience'),
    rule('YEARS_EXPERIENCE_REQUIRED', r'multi(ple)?\b.*\byears?\b.*\bexperience'),
    rule('ADVANCED_REQUIRED', r'(proficien(cy|t)|fluen(cy|t)|well.?versed) (in|with|\w+ing)'),
    rule('ADVANCED_REQUIRED', r'responsibility\b.*\bfor\b.*\b(architecture|design)'),
    rule('ADVANCED_REQUIRED', r'experience\b.*\beverything else'),
    rule('ADVANCED_REQUIRED', r'experience\b.*\bwith\b.*\bvariety'),
    rule('ADVANCED_REQUIRED', r'experienced?\b.*\bas\b.*\b(engineer|developer)'),
    rule('ADVANCED_REQUIRED', r'you\b.*\b(consider yourself|are)\b.*\b(expert|researcher|hacker)'),
    rule('ADVANCED_REQUIRED', r'self-starter'),
    rule('ADVANCED_REQUIRED', r'take\b.*\b(ownership|responsibility)'),
    rule('ADVANCED_REQUIRED', r'manage\b.*\bpriorities'),
    rule('ADVANCED_REQUIRED', r'translate\b.*\bbusiness'),
    rule('ADVANCED_REQUIRED', r'analysis\b.*\bexperience'),
    rule('ADVANCED_REQUIRED', r'have\b.*\bsuperpowers?'),
    rule('ADVANCED_REQUIRED', r'must have\b.*\bexperience'),
    rule('ADVANCED_REQUIRED', r'previous experience with'),
    rule('ADVANCED_REQUIRED', r'(provable|relevant)\b.*\bindustry experience'),
    rule('LEADERSHIP_REQUIRED', r'(leadership|mentoring)\b.*\b(experience|skills)'),
    rule('LEADERSHIP_REQUIRED', r'experience\b.*\b(leading|leader)'),
    rule('LEADERSHIP_REQUIRED', r'lead(ing)?\b.*\b(teams?|courses?)'),
    rule('LEADERSHIP_REQUIRED', r'lead(ing)?\b.*\bby example'),
    rule('LEADERSHIP_REQUIRED', r'delegat\w+\b.*\bothers'),
    rule('LEADERSHIP_REQUIRED', r'mentor(ing)?\b.*\bjunio\w+'),
    rule('INDEPENDENCE_PREFERRED', r'(execute|work(ing)?|operat(e|ing)|solv(e|ing))\b.*\b(independen\w+|autonomou\w+)'),
    rule('INDEPENDENCE_PREFERRED', r'(independent|autonomous)\b.*\bworking'),
    rule('INDEPENDENCE_PREFERRED', r'(little|minimal|minimum)\b.*\bsupervision'),
    rule('INDEPENDENCE_PREFERRED', r'self.?sufficient'),
    rule('EXPLICITLY_SENIOR', r'senior'),
    rule('EXPLICITLY_JUNIOR', r'junior'),
    rule('JUNIOR_FRIENDLY', r'do(es)?(n.?t| not) matter'),
    rule('JUNIOR_FRIENDLY', r'entry.?level'),
    rule('JUNIOR_FRIENDLY', r'learn a (lot|ton)'),
    rule('JUNIOR_FRIENDLY', r'whether\b.*\byou\b.*\bknow\b.*\bor\b.*\bnot(hing)?'),
    rule('JUNIOR_FRIENDLY', r'you\b.*\bmissing'),
    rule('JUNIOR_FRIENDLY', r'start\b.*\bcareer'),
    rule('JUNIOR_FRIENDLY', r'school\b.*\bprojects?'),
    rule('JUNIOR_FRIENDLY', r'(under|with)\b.*\b(guidance|support)'),
    rule('JUNIOR_FRIENDLY', r'not?\b.*\bnecessar(y|ily)'),
    rule('JUNIOR_FRIENDLY', r'open\b.*\bgraduat\w+'),
    rule('JUNIOR_FRIENDLY', r'not?\b.*\bbig deal'),
    rule('JUNIOR_FRIENDLY', r'(educational|school)\b.*\bexperience'),
    rule('LEARNING_REQUIRED', r'will\w*\b.*\bto\b.*\blearn'),
]
SUPPRESSING_RULES_EN = [
    rule('', r'(is|are|would be|as)( an?)? ((big )?plus|benefit|advantage)'),
    rule('', r'we welcome'),
    rule('', r'nice to have'),
    rule('', r'an? advantage'),
    rule('', r'training'),
    rule('TECH_DEGREE_REQUIRED', r'or\b.*\bequivalent\b.*\bexperience'),
    rule('ADVANCED_REQUIRED', r'communications? skills'),
    rule('ADVANCED_REQUIRED', r'english'),
    rule('ADVANCED_REQUIRED', r'depend(s|ing) on your'),
    rule('ADVANCED_REQUIRED', r'(ms|microsoft) office'),
    rule('ADVANCED_REQUIRED', r'not?\b.*\bnecessary'),
    rule('ADVANCED_REQUIRED', r'(user|developer) experience'),
    rule('ADVANCED_REQUIRED', r'if\b.*\binterested'),
    rule('ADVANCED_REQUIRED', r'send us'),
    rule('ADVANCED_REQUIRED', r'apply'),
    rule('ADVANCED_REQUIRED', r'(professional|personal) (requirements|skills)'),
    rule('ADVANCED_REQUIRED', r'(educational|school)\b.*\bexperience'),
    rule('EXPLICITLY_SENIOR', r'junior'),
    rule('EXPLICITLY_JUNIOR', r'(senior|mentor)'),
    rule('CZECH_REQUIRED', r'courses?'),
    rule('SLOVAK_REQUIRED', r'courses?'),
    rule('GERMAN_REQUIRED', r'courses?'),
    rule('LEADERSHIP_REQUIRED', r'(industry|join)'),
]


ADVANCED_SKILLS_ADJECTIVES_CS = [r'pokročil\w+', r'výborn\w+', r'skvěl\w+',
                                 r'komerční', r'dobr\w+', r'perfekt\w*']
SKILLS_NOUNS_CS = [r'znalost\w*', r'zkušenost\w*', r'myšlení']
TECH_DEGREES_CS = [r'vysokoškol\w+', r'vš', r'studi(um|a|i)', r'titul\w*',
                   r'absolven\w+']
TECH_DEGREE_FIELDS_CS = [r'techn\w+', r'informati\w+', r'it']


RULES_CS = (
    rules('ADVANCED_REQUIRED', ADVANCED_SKILLS_ADJECTIVES_CS, SKILLS_NOUNS_CS) +
    rules('JUNIOR_FRIENDLY', SKILLS_NOUNS_CS, [r'programovací\w*\b.*\bjazyk\w*']) +
    rules('LEADERSHIP_REQUIRED', SKILLS_NOUNS_CS, [r'(vedení\w*|vést)\b.*\btým\w*']) +
    rules('TECH_DEGREE_REQUIRED', TECH_DEGREES_CS, TECH_DEGREE_FIELDS_CS, any_order=True)
) + [
    rule('YEARS_EXPERIENCE_REQUIRED', r'(a(le)?spoň|minim\w+|min|\d+)[\W]*(rok|let|rok[yůu])'),
    rule('ENGLISH_REQUIRED', r'(angličtin\w+|anglick\w+)'),
    rule('ENGLISH_REQUIRED', r'AJ', ignorecase=False),
    rule('ENGLISH_REQUIRED', r'EN', ignorecase=False),
    rule('GERMAN_REQUIRED', r'NJ', ignorecase=False),
    rule('GERMAN_REQUIRED', r'(němčin\w+|německ\w+)'),
    rule('ADVANCED_REQUIRED', r'zkušenos\w+\b.*\b(vývíje|vývoj)\w+'),
    rule('ADVANCED_REQUIRED', r'nejsi\b.*\bzelenáč'),
    rule('ADVANCED_REQUIRED', r'(rozhled\w*|prax\w+|architekt\w*)'),
    rule('ADVANCED_REQUIRED', r'máš\b.*\bza sebou'),
    rule('ADVANCED_REQUIRED', r'samostatn\w+\b.*\břeš\w+\b.*\bproblém\w+'),
    rule('EXPLICITLY_SENIOR', r'(seniorní|senior)'),
    rule('EXPLICITLY_JUNIOR', r'(junior|jnr|juniorní\w*)'),
    rule('INDEPENDENCE_PREFERRED', r'samostatn\w+|individuáln\w+'),
    rule('JUNIOR_FRIENDLY', r'naučí(me|š)'),
    rule('JUNIOR_FRIENDLY', r'(prostor\w*|příležitost\w*|možnost\w*)\b.*\bučit'),
    rule('JUNIOR_FRIENDLY', r'(absolvent\w*|studuješ|ze školy|školní)'),
    rule('JUNIOR_FRIENDLY', r'a(le)?spoň\b.*\bzákladní'),
    rule('JUNIOR_FRIENDLY', r'(nem[aá]\w*|nemusí\w*)\b.*\b(zkušen\w*|umět)'),
    rule('JUNIOR_FRIENDLY', r'práce\b.*\bPC', ignorecase=False),
    rule('JUNIOR_FRIENDLY', r'\w*start\w*\b.*\bkariér\w+'),
    rule('LEARNING_REQUIRED', r'(chce\w*|chtěj\w*|chuť|ochot\w+|schopn\w+)\b.*\b(učit|na sobě|rozvíj\w+)'),
]
SUPPRESSING_RULES_CS = [
    rule('', r'výhodou'),
    rule('EXPLICITLY_SENIOR', r'(junior|jnr|juniorní\w*)'),
    rule('EXPLICITLY_JUNIOR', r'(seniorní|senior)'),
    rule('ENGLISH_REQUIRED', r'(výuk\w|kurz\w*)'),
    rule('GERMAN_REQUIRED', r'(výuk\w|kurz\w*)'),
    rule('ADVANCED_REQUIRED', r'škol\w+'),
    rule('TECH_DEGREE_REQUIRED', r'(či|nebo)\b.*\bprax\w+'),
    rule('TECH_DEGREE_REQUIRED', r'nerozhoduje'),
]


RULES = {'en': RULES_EN, 'cs': RULES_CS}
SUPPRESSING_RULES = {'en': SUPPRESSING_RULES_EN, 'cs': SUPPRESSING_RULES_CS}


class Pipeline():
    def process_item(self, item, spider):
        features = []
        features.append((LANG_MAPPING[item['lang']], None, None))
        features.extend(parse_from_sentence(item['title'], item['lang']))
        features.extend(parse_from_sentences(item['description_sentences'],
                                             item['lang']))
        item['features'] = features
        return item


def parse_from_sentences(sentences, lang):
    return itertools.chain.from_iterable(parse_from_sentence(sentence, lang)
                                         for sentence in sentences)


def parse_from_sentence(sentence, lang):
    for rule_id, rule_re in RULES[lang]:
        match = rule_re.search(sentence)
        # print(rule_re.pattern, match)
        if (match and
            not is_supressed(rule_id, sentence, lang)):
            yield (rule_id, sentence, match.group(0))


def is_supressed(rule_id, sentence, lang):
    for suppressing_rule_id, suppressing_rule_re in SUPPRESSING_RULES[lang]:
        is_relevant = (suppressing_rule_id == '' or
                       suppressing_rule_id == rule_id)
        if is_relevant and suppressing_rule_re.search(sentence):
            return True
    return False
