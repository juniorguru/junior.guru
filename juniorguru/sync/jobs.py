import os
import json
from itertools import islice
from pathlib import Path
from datetime import date
from queue import Empty
from multiprocessing import Process, JoinableQueue as Queue
from pprint import pformat
from peewee import IntegrityError

from juniorguru.lib import timer, loggers
from juniorguru.models import db, Job
from juniorguru.jobs.settings import FEEDS_DIR


logger = loggers.get('juniorguru.sync.jobs')


TRAILING_DAYS = 365
PROCESSING_CHUNKSIZE = 10


# TODO musi umet pracovat s tim, ze jsou data odminule, uz probehl sync-jobs jednou a ted se spustil znova aby syncnul increment


@timer.measure('jobs')
def main():
    with db:
        Job.drop_table()
        Job.create_table()

    logger.debug("Detecting .jsonl files")
    paths = list(Path(FEEDS_DIR).glob('**/*.jsonl'))

    logger.debug(f"Detecting relevant directories for {TRAILING_DAYS} past days")
    dirs = {path.parent for path in paths}
    dirs = sorted(dirs, reverse=True)[:TRAILING_DAYS]
    logger.debug(f"Detected {len(dirs)} relevant directories")
    paths = [path for path in paths if path.parent in dirs]
    logger.debug(f"Detected {len(paths)} relevant .jsonl files")

    logger.info("Processing items")
    path_queue = Queue()
    for path in paths:
        path_queue.put(path)
    item_queue = Queue()
    Process(target=writer, args=(item_queue,), daemon=True).start()
    readers = []
    readers_count = os.cpu_count()
    for reader_n in range(readers_count):
        proc = Process(target=reader, args=(reader_n, path_queue, item_queue))
        readers.append(proc)
        proc.start()
    for proc in readers:
        proc.join()
    item_queue.join()


def reader(reader_n, path_queue, item_queue):
    reader_logger = logger.getChild(f'readers.{reader_n}')
    reader_logger.debug("Starting")
    try:
        while True:
            path = path_queue.get(timeout=1)
            reader_logger.debug(f"Parsing {path}")
            counter = 0
            for item in parse(path):
                item_queue.put(item)
                counter += 1
            reader_logger.info(f"Parsed {path} into {counter} items")
            path_queue.task_done()
    except Empty:
        reader_logger.debug("Nothing else to parse, closing")


def writer(item_queue):
    writer_logger = logger.getChild('writer')
    writer_logger.debug("Starting")
    try:
        while True:
            item = item_queue.get()
            writer_logger.debug(f"Saving {item['url']}")
            with db:
                job = Job.from_item(item)
                try:
                    job.save()
                except IntegrityError:
                    job = Job.get_by_item(item)
                    job.merge_item(item)
                    job.save()
                except Exception:
                    writer_logger.error(f'Error saving the following item:\n{pformat(item)}')
                    raise
            writer_logger.debug(f"Saved {job.url} as {job.id}")
            item_queue.task_done()
    finally:
        writer_logger.debug("Closing writer")


def parse(path):
    parse_logger = logger.getChild('parse')
    with path.open() as f:
        for line_no, line in enumerate(f, start=1):
            try:
                data = json.loads(line)
                data['first_seen_on'] = date.fromisoformat(data['first_seen_on'])
                data['last_seen_on'] = path_to_date(path)
            except Exception:
                parse_logger.error(f'Error parsing the following data:\n\n{line}\n\n'
                                   f'Line number: {line_no}, file: {path}')
                raise
            yield data


def chunk(paths, size):
    return iter(lambda: list(islice(paths, size)), [])


def path_to_date(path):
    return date(year=int(path.parent.parent.parent.stem),
                month=int(path.parent.parent.stem),
                day=int(path.parent.stem))


if __name__ == '__main__':
    main()
