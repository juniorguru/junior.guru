import itertools
import json
from pathlib import Path
from datetime import date
from multiprocessing import Pool

from juniorguru.lib import timer, loggers
from juniorguru.models import with_db
from juniorguru.jobs.settings import FEEDS_DIR


logger = loggers.get('jobs')


DATA_LIMIT_DAYS = 365


@timer.measure('jobs')
@with_db
def main():
    # TODO musi umet pracovat s tim, ze jsou data odminule, uz probehl sync-jobs jednou a ted se spustil znova aby syncnul increment
    paths = list(Path(FEEDS_DIR).glob('**/*.jsonl'))

    dirs = {path.parent for path in paths}
    dirs = sorted(dirs, reverse=True)[:DATA_LIMIT_DAYS]

    items_generators = (parse(path) for path in paths if path.parent in dirs)
    items = itertools.chain.from_iterable(items_generators)
    Pool().map(process, items)


def process(item):
    print(item)


def parse(path):
    with path.open() as f:
        for line in f:
            data = json.loads(line)
            data['seen_on'] = path_to_date(path)
            yield data


def path_to_date(path):
    return date(year=int(path.parent.parent.parent.stem),
                month=int(path.parent.parent.stem),
                day=int(path.parent.stem))


if __name__ == '__main__':
    main()
