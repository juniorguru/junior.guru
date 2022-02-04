import os
from pathlib import Path

from juniorguru.lib.timer import measure
from juniorguru.models import db, Job
from juniorguru.jobs.settings import FEEDS_DIR
from juniorguru.sync.jobs.processing import filter_relevant_paths, process_paths


TRAILING_DAYS = 365

PIPELINES = {

}


@measure('jobs')
def main():
    with db:
        Job.drop_table()
        Job.create_table()

    paths = Path(FEEDS_DIR).glob('**/*.jsonl')
    paths = filter_relevant_paths(paths, TRAILING_DAYS)
    process_paths(paths, PIPELINES, workers=os.cpu_count())


main()
