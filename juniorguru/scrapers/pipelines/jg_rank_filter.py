import itertools


WEIGHTS = {
    'EXPLICITLY_SENIOR': -8,
    'YEARS_EXPERIENCE_REQUIRED': -8,
    'LEADERSHIP_REQUIRED': -8,
    'TECH_DEGREE_REQUIRED': -6,
    'ADVANCED_REQUIRED': -4,
    'INDEPENDENCE_PREFERRED': -2,
    'ENGLISH_REQUIRED': 0,
    'CZECH_REQUIRED': 0,
    'SLOVAK_REQUIRED': 0,
    'GERMAN_REQUIRED': 0,
    'LEARNING_REQUIRED': 2,
    'JUNIOR_FRIENDLY': 4,
    'EXPLICITLY_JUNIOR': 6,
}
RELEVANT_FEATURES = {feature for feature, weight
                     in WEIGHTS.items() if weight}
ACCUMULATIVE_FEATURES = {
    'YEARS_EXPERIENCE_REQUIRED',
    'ADVANCED_REQUIRED',
    'INDEPENDENCE_PREFERRED',
    'LEARNING_REQUIRED',
    'JUNIOR_FRIENDLY',
}
FEW_FEATURES_THRESHOLD = 2
FEW_FEATURES_PENALTY = 0.5


class Pipeline():
    def process_item(self, item, spider):
        item['jg_rank'] = calc_jg_rank([feature['name'] for feature
                                        in item['features']])
        return item


def calc_jg_rank(features):
    # - zapocitat nejak ze cislo vznika z nula nebo jedne-dvou feautres, /2
    #   a taky co to je za features, jestli cummulative drobny nebo silny
    features = [f for f in features if f in RELEVANT_FEATURES]
    grades = [WEIGHTS[f] for f in itertools.chain(
        (f for f in features if f in ACCUMULATIVE_FEATURES),
        (f for f in frozenset(features) - ACCUMULATIVE_FEATURES),
    )]
    grades_count = len(grades)
    rank = sum(grades)

    # if rank is calculated from more than FEW_FEATURES_THRESHOLD features,
    # then multiply it by two so that ranks calculated from low numbers
    # of features effectively get a penalty
    if grades_count > FEW_FEATURES_THRESHOLD:
        rank *= int(1 / FEW_FEATURES_PENALTY)

    return rank
