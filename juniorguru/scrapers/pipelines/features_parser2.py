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


def rule(identifier, *patterns, ignorecase=True, any_order=False):
    compile_flags = re.IGNORECASE if ignorecase else 0
    pattern_lists = [([pattern] if isinstance(pattern, str) else list(pattern))
                     for pattern in patterns]
    if any_order:
        permutations = itertools.permutations(pattern_lists)
    else:
        permutations = [pattern_lists]
    for pattern_lists in permutations:
        for patterns_tuple in itertools.product(*pattern_lists):
            pattern = FOLLOWED_BY_PATTERN.join(patterns_tuple)
            rule_re = re.compile(''.join([
                # implicit boundary if not ^
                '' if pattern[0] == '^' else r'\b',
                # pattern itself
                pattern,
                # implicit boundary if not $
                '' if pattern[-1] == '$' else r'\b',
            ]), compile_flags)
            yield (identifier, rule_re)


def rules(rules):
    return list(itertools.chain.from_iterable(rules))


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


RULES_EN = rules([
    rule('TECH_DEGREE_REQUIRED', TECH_DEGREES_EN + [r'degree', r'studies'], TECH_DEGREE_FIELDS_EN),
    rule('TECH_DEGREE_REQUIRED', r'completed', r'education', TECH_DEGREE_FIELDS_EN),
    rule('TECH_DEGREE_REQUIRED', TECH_DEGREE_FIELDS_EN, [r'degree', r'education', r'university']),
    rule('TECH_DEGREE_REQUIRED', TECH_DEGREES_EN, [r'degree', r'or higher']),
    rule('TECH_DEGREE_REQUIRED', r'academic record'),
    rule('YEARS_EXPERIENCE_REQUIRED', r'[\d\-\+ ]+[^\d]+years?.?', r'(experience|track record)'),
    rule('YEARS_EXPERIENCE_REQUIRED', r'experience\b.*[\d\-\+ ]+[^\d]+years?.?'),
    rule('YEARS_EXPERIENCE_REQUIRED', r'[\d\+] experience'),
    rule('YEARS_EXPERIENCE_REQUIRED', r'multi(ple)?', r'years?', r'experience'),
    rule('ADVANCED_REQUIRED', ADVANCED_SKILLS_ADJECTIVES_EN, SKILLS_NOUNS_EN),
    rule('ADVANCED_REQUIRED', r'experience', [r'architect\w+', r'building', r'consuming', r'deploy\w+']),
    rule('ADVANCED_REQUIRED', [r'commercial', r'solid', r'work', r'working', r'previous', r'implementation', r'hands-on', r'architect\w+'], [r'experience', r'knowledge']),
    rule('ADVANCED_REQUIRED', r'(proficien(cy|t)|fluen(cy|t)|well.?versed) (in|with|\w+ing)'),
    rule('ADVANCED_REQUIRED', r'responsibility', r'for', r'(architecture|design)'),
    rule('ADVANCED_REQUIRED', r'experience', r'everything else'),
    rule('ADVANCED_REQUIRED', r'experience', r'with', r'variety'),
    rule('ADVANCED_REQUIRED', r'experienced?', r'as', r'(engineer|developer)'),
    rule('ADVANCED_REQUIRED', r'you', r'(consider yourself|are)', r'(expert|researcher|hacker)'),
    rule('ADVANCED_REQUIRED', r'self-starter'),
    rule('ADVANCED_REQUIRED', r'take', r'(ownership|responsibility)'),
    rule('ADVANCED_REQUIRED', r'manage', r'priorities'),
    rule('ADVANCED_REQUIRED', r'translate', r'business'),
    rule('ADVANCED_REQUIRED', r'analysis', r'experience'),
    rule('ADVANCED_REQUIRED', r'have', r'superpowers?'),
    rule('ADVANCED_REQUIRED', r'must have', r'experience'),
    rule('ADVANCED_REQUIRED', r'previous experience with'),
    rule('ADVANCED_REQUIRED', r'(provable|relevant)', r'industry experience'),
    rule('LEADERSHIP_REQUIRED', r'(leadership|mentoring)', r'(experience|skills)'),
    rule('LEADERSHIP_REQUIRED', r'experience', r'(leading|leader)'),
    rule('LEADERSHIP_REQUIRED', r'lead(ing)?', r'(teams?|courses?)'),
    rule('LEADERSHIP_REQUIRED', r'lead(ing)?', r'by example'),
    rule('LEADERSHIP_REQUIRED', r'delegat\w+', r'others'),
    rule('LEADERSHIP_REQUIRED', r'mentor(ing)?', r'junio\w+'),
    rule('INDEPENDENCE_PREFERRED', r'(execute|work(ing)?|operat(e|ing)|solv(e|ing))', r'(independen\w+|autonomou\w+)'),
    rule('INDEPENDENCE_PREFERRED', r'(independent|autonomous)', r'working'),
    rule('INDEPENDENCE_PREFERRED', r'(little|minimal|minimum)', r'supervision'),
    rule('INDEPENDENCE_PREFERRED', r'self.?sufficient'),
    rule('EXPLICITLY_SENIOR', r'senior'),
    rule('EXPLICITLY_SENIOR', [r'seasoned', r'experienced', r'practiced'], [r'engineer', r'developer']),
    rule('EXPLICITLY_JUNIOR', r'junior'),
    rule('JUNIOR_FRIENDLY', r'do(es)?(n.?t| not) matter'),
    rule('JUNIOR_FRIENDLY', r'entry.?level'),
    rule('JUNIOR_FRIENDLY', r'learn a (lot|ton)'),
    rule('JUNIOR_FRIENDLY', r'whether', r'you', r'know', r'or', r'not(hing)?'),
    rule('JUNIOR_FRIENDLY', r'you', r'missing'),
    rule('JUNIOR_FRIENDLY', r'start', r'career'),
    rule('JUNIOR_FRIENDLY', r'school', r'projects?'),
    rule('JUNIOR_FRIENDLY', r'(under|with)', r'(guidance|support)'),
    rule('JUNIOR_FRIENDLY', r'not?', r'necessar(y|ily)'),
    rule('JUNIOR_FRIENDLY', r'open', r'graduat\w+'),
    rule('JUNIOR_FRIENDLY', r'not?', r'big deal'),
    rule('JUNIOR_FRIENDLY', r'(educational|school)', r'experience'),
    rule('LEARNING_REQUIRED', r'will\w*', r'to', r'learn'),
    rule('CZECH_REQUIRED', r'czech', LANGUAGE_KEYWORDS_EN, any_order=True),
    rule('SLOVAK_REQUIRED', r'slovak', LANGUAGE_KEYWORDS_EN, any_order=True),
    rule('GERMAN_REQUIRED', r'german', LANGUAGE_KEYWORDS_EN, any_order=True),
])
SUPPRESSING_RULES_EN = rules([
    rule('', r'(is|are|would be|as)( an?)? ((big )?plus|benefit|advantage)'),
    rule('', r'we welcome'),
    rule('', r'nice to have'),
    rule('', r'an? advantage'),
    rule('', r'training'),
    rule('TECH_DEGREE_REQUIRED', r'or', r'equivalent', r'experience'),
    rule('ADVANCED_REQUIRED', r'communications? skills'),
    rule('ADVANCED_REQUIRED', r'english'),
    rule('ADVANCED_REQUIRED', r'depend(s|ing) on your'),
    rule('ADVANCED_REQUIRED', r'(ms|microsoft) office'),
    rule('ADVANCED_REQUIRED', r'not?', r'necessary'),
    rule('ADVANCED_REQUIRED', r'(user|developer) experience'),
    rule('ADVANCED_REQUIRED', r'if', r'interested'),
    rule('ADVANCED_REQUIRED', r'send us'),
    rule('ADVANCED_REQUIRED', r'apply'),
    rule('ADVANCED_REQUIRED', r'(professional|personal) (requirements|skills)'),
    rule('ADVANCED_REQUIRED', r'(educational|school)', r'experience'),
    rule('EXPLICITLY_SENIOR', r'junior'),
    rule('EXPLICITLY_JUNIOR', r'(senior|mentor)'),
    rule('CZECH_REQUIRED', r'courses?'),
    rule('SLOVAK_REQUIRED', r'courses?'),
    rule('GERMAN_REQUIRED', r'courses?'),
    rule('LEADERSHIP_REQUIRED', r'(industry|join)'),
])


ADVANCED_SKILLS_ADJECTIVES_CS = [r'pokročil\w+', r'výborn\w+', r'skvěl\w+',
                                 r'komerční', r'dobr\w+', r'perfekt\w*']
SKILLS_NOUNS_CS = [r'znalost\w*', r'zkušenost\w*', r'myšlení']
TECH_DEGREES_CS = [r'vysokoškol\w+', r'vš', r'studi(um|a|i)', r'titul\w*',
                   r'absolven\w+']
TECH_DEGREE_FIELDS_CS = [r'techn\w+', r'informati\w+', r'it']


RULES_CS = rules([
    rule('JUNIOR_FRIENDLY', SKILLS_NOUNS_CS, r'programovací\w*', r'jazyk\w*'),
    rule('LEADERSHIP_REQUIRED', SKILLS_NOUNS_CS, r'(vedení\w*|vést)', r'tým\w*'),
    rule('TECH_DEGREE_REQUIRED', TECH_DEGREES_CS, TECH_DEGREE_FIELDS_CS, any_order=True),
    rule('ADVANCED_REQUIRED', ADVANCED_SKILLS_ADJECTIVES_CS, SKILLS_NOUNS_CS),
    rule('YEARS_EXPERIENCE_REQUIRED', r'(a(le)?spoň|minim\w+|min|\d+)[\W]*(rok|let|rok[yůu])'),
    rule('ENGLISH_REQUIRED', r'(angličtin\w+|anglick\w+)'),
    rule('ENGLISH_REQUIRED', r'AJ', ignorecase=False),
    rule('ENGLISH_REQUIRED', r'EN', ignorecase=False),
    rule('GERMAN_REQUIRED', r'NJ', ignorecase=False),
    rule('GERMAN_REQUIRED', r'(němčin\w+|německ\w+)'),
    rule('ADVANCED_REQUIRED', r'zkušenos\w+', r'(vývíje|vývoj)\w+'),
    rule('ADVANCED_REQUIRED', r'nejsi', r'zelenáč'),
    rule('ADVANCED_REQUIRED', r'(rozhled\w*|prax\w+|architekt\w*)'),
    rule('ADVANCED_REQUIRED', r'máš', r'za sebou'),
    rule('ADVANCED_REQUIRED', r'samostatn\w+', r'řeš\w+', r'problém\w+'),
    rule('EXPLICITLY_SENIOR', r'(seniorní|senior)'),
    rule('EXPLICITLY_JUNIOR', r'(junior|jnr|juniorní\w*)'),
    rule('INDEPENDENCE_PREFERRED', r'samostatn\w+|individuáln\w+'),
    rule('JUNIOR_FRIENDLY', r'naučí(me|š)'),
    rule('JUNIOR_FRIENDLY', r'(prostor\w*|příležitost\w*|možnost\w*)', r'učit'),
    rule('JUNIOR_FRIENDLY', r'(absolvent\w*|studuješ|ze školy|školní)'),
    rule('JUNIOR_FRIENDLY', r'a(le)?spoň', r'základní'),
    rule('JUNIOR_FRIENDLY', r'(nem[aá]\w*|nemusí\w*)', r'(zkušen\w*|umět)'),
    rule('JUNIOR_FRIENDLY', r'práce', r'PC', ignorecase=False),
    rule('JUNIOR_FRIENDLY', r'\w*start\w*', r'kariér\w+'),
    rule('LEARNING_REQUIRED', r'(chce\w*|chtěj\w*|chuť|ochot\w+|schopn\w+)', r'(učit|na sobě|rozvíj\w+)'),
])
SUPPRESSING_RULES_CS = rules([
    rule('', r'výhodou'),
    rule('EXPLICITLY_SENIOR', r'(junior|jnr|juniorní\w*)'),
    rule('EXPLICITLY_JUNIOR', r'(seniorní|senior)'),
    rule('ENGLISH_REQUIRED', r'(výuk\w|kurz\w*)'),
    rule('GERMAN_REQUIRED', r'(výuk\w|kurz\w*)'),
    rule('ADVANCED_REQUIRED', r'škol\w+'),
    rule('TECH_DEGREE_REQUIRED', r'(či|nebo)', r'prax\w+'),
    rule('TECH_DEGREE_REQUIRED', r'nerozhoduje'),
])


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
        print(rule_re.pattern, match)
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
