from pathlib import Path
from queue import Empty
from multiprocessing import Process, JoinableQueue as Queue
import json
from datetime import date

from pprint import pformat
from peewee import IntegrityError

from juniorguru.lib import loggers
from juniorguru.models import db, Job


logger = loggers.get('juniorguru.sync.jobs')


def filter_relevant_paths(paths, trailing_days):
    paths = [Path(path) for path in paths]
    logger.debug(f"Filtering {len(paths)} .jsonl files")
    logger.debug(f"Detecting relevant directories for {trailing_days} past days")
    dirs = {path.parent for path in paths}
    dirs = sorted(dirs, reverse=True)[:trailing_days]
    logger.debug(f"Detected {len(dirs)} relevant directories")
    paths = [path for path in paths if path.parent in dirs]
    logger.debug(f"Detected {len(paths)} relevant .jsonl files")
    return paths


# TODO musi umet pracovat s tim, ze jsou data odminule, uz probehl sync-jobs jednou a ted se spustil znova aby syncnul increment
def process_paths(paths, pipelines, workers=1):
    path_queue = Queue()
    for path in paths:
        path_queue.put(path)
    item_queue = Queue()
    Process(target=_writer, args=(item_queue,), daemon=True).start()
    readers = []
    for reader_n in range(workers):
        proc = Process(target=_reader, args=(reader_n, path_queue, item_queue, pipelines))
        readers.append(proc)
        proc.start()
    for proc in readers:
        proc.join()
    item_queue.join()


def _reader(reader_n, path_queue, item_queue, pipelines):
    reader_logger = logger.getChild(f'readers.{reader_n}')
    reader_logger.debug("Starting")
    # pipelines = load_pipelines(pipelines)
    try:
        while True:
            path = path_queue.get(timeout=1)
            reader_logger.debug(f"Parsing {path}")
            counter = 0
            for item in parse(path):
                # item = execute_pipelines(item, pipelines)
                item_queue.put(item)
                counter += 1
            reader_logger.info(f"Parsed {path} into {counter} items")
            path_queue.task_done()
    except Empty:
        reader_logger.debug("Nothing else to parse, closing")


def _writer(item_queue):
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
    with path.open() as f:
        for line_no, line in enumerate(f, start=1):
            yield parse_line(path, line_no, line)


def parse_line(path, line_no, line):
    try:
        data = json.loads(line)
        data['first_seen_on'] = date.fromisoformat(data['first_seen_on'])
        data['last_seen_on'] = path_to_date(path)
        return data
    except Exception:
        parse_logger = logger.getChild('parse')
        parse_logger.error(f'Error parsing the following data:\n\n{line}\n\n'
                            f'Line number: {line_no}, file: {path}')
        raise


def path_to_date(path):
    return date(year=int(path.parent.parent.parent.stem),
                month=int(path.parent.parent.stem),
                day=int(path.parent.stem))
