import itertools
from math import floor

from scrapy.exceptions import DropItem


class NotEntryLevel(DropItem):
    pass


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

MIN_JG_RANK = 1


class Pipeline():
    def process_item(self, item, spider):
        jg_rank = calc_jg_rank([feature['name'] for feature
                                in item['features']])
        item['jg_rank'] = jg_rank
        if jg_rank < MIN_JG_RANK:
            raise NotEntryLevel(f"JG rank is {jg_rank} (minimum: {MIN_JG_RANK})")
        return item


def calc_jg_rank(features):
    features = [f for f in features if f in RELEVANT_FEATURES]
    features = list(itertools.chain(
        (f for f in features if f in ACCUMULATIVE_FEATURES),
        (f for f in frozenset(features) - ACCUMULATIVE_FEATURES),
    ))
    if len(features) <= 1:
        return 0
    if len(features) <= FEW_FEATURES_THRESHOLD:
        return sum([int(WEIGHTS[f] / abs(WEIGHTS[f])) for f in features])
    return sum([WEIGHTS[f] for f in features])
