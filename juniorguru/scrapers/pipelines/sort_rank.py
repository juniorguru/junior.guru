import math
from datetime import date


BUMP_PERIOD_DAYS = 30
WEIGHTS = {
    'favoritism': 1,
    'freshness': 1,
    'juniority': 1,
}


class Pipeline():
    def __init__(self, today=None):
        self.today = today or date.today()

    def process_item(self, item, spider):
        components = {
            'favoritism': calc_favoritism(item.get('pricing_plan')),
            'freshness': calc_freshness(item['posted_at'], self.today),
            'juniority': calc_juniority(item['junior_rank']),
        }
        item['sort_rank_components'] = components
        item['sort_rank'] = calc_sort_rank(components, WEIGHTS)
        return item


def calc_sort_rank(components, weights):
    return sum([weights[name] * value for name, value in components.items()])


def calc_favoritism(pricing_plan):
    return dict(standard=90, annual_flat_rate=100).get(pricing_plan, 0)


def calc_freshness(posted_at, today):
    days = (today - posted_at).days % BUMP_PERIOD_DAYS
    return math.ceil(((BUMP_PERIOD_DAYS - days) * 100) / BUMP_PERIOD_DAYS)


def calc_juniority(junior_rank):
    if junior_rank < 0:
        return 0
    if 0 <= junior_rank < 4:
        return 25
    if 4 <= junior_rank < 10:
        return 50
    if 10 <= junior_rank < 18:
        return 75
    return 100
