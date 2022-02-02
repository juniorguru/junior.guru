import itertools
import json
from pathlib import Path
from datetime import date
from multiprocessing import Pool

from juniorguru.lib import timer, loggers
from juniorguru.models import with_db, Job
from juniorguru.jobs.settings import FEEDS_DIR


logger = loggers.get('juniorguru.sync.jobs')


TRAILING_DAYS = 365
POOL_CHUNKSIZE = 10


@timer.measure('jobs')
@with_db
def main():
    # TODO musi umet pracovat s tim, ze jsou data odminule, uz probehl sync-jobs jednou a ted se spustil znova aby syncnul increment
    logger.debug("Detecting .jsonl files")
    paths = list(Path(FEEDS_DIR).glob('**/*.jsonl'))

    logger.debug(f"Detecting relevant directories for {TRAILING_DAYS} past days")
    dirs = {path.parent for path in paths}
    dirs = sorted(dirs, reverse=True)[:TRAILING_DAYS]
    logger.debug(f"Detected {len(dirs)} relevant directories")

    items_generators = (parse(path) for path in paths if path.parent in dirs)
    items = itertools.chain.from_iterable(items_generators)

    logger.info("Processing items")
    for job in Pool().imap_unordered(process, items, chunksize=POOL_CHUNKSIZE):
        # job.save()
        pass


def process(item):
    logger.debug(f"Processing {item['url']}")
    # print(item)
    # return Job()


def parse(path):
    logger.debug(f"Opening {path}")
    with path.open() as f:
        for line in f:
            data = json.loads(line)
            data['seen_on'] = path_to_date(path)
            yield data
        logger.debug(f"Closing {path}")


def path_to_date(path):
    return date(year=int(path.parent.parent.parent.stem),
                month=int(path.parent.parent.stem),
                day=int(path.parent.stem))


if __name__ == '__main__':
    main()
