from juniorguru.lib import loggers
from juniorguru.lib.locations import fetch_locations


logger = loggers.get(__name__)


def process(item, **kwargs):
    debug_info = dict(title=item.get('title'), company=item.get('company_name'))
    locations_raw = item['locations_raw'] or []
    item['locations'] = fetch_locations(locations_raw, debug_info=debug_info, **kwargs)
    return item
