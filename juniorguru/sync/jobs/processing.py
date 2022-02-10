import importlib
import os
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


WORKERS = os.cpu_count()


class DropItem(Exception):
    pass


# TODO musi umet pracovat s tim, ze jsou data odminule, uz probehl sync-jobs jednou a ted se spustil znova aby syncnul increment
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


def process_paths(paths, pipelines, workers=None):
    workers = workers or WORKERS

    # First we create the path queue and fill it with paths pointing
    # at .jsonl files we want to parse. Then we create the item queue,
    # which will collect parsed items. The writer process starts, waiting
    # for the item queue. The process being deamon means that it's going
    # to be terminated automatically once this program is done and doesn't
    # need to be managed manually. Reader processes get started, pop paths
    # from the path queue, stream the .jsonl files, parse each line, and
    # put individual items to the item queue. From there the writer process
    # takes care of saving them to the db and merging the same jobs. This
    # intentionally happens in a single process so that SQLite isn't
    # overloaded by concurrent writes.

    path_queue = Queue()
    for path in paths:
        path_queue.put(path)

    item_queue = Queue()
    Process(target=_writer, args=(item_queue,), daemon=True).start()

    readers = []
    for reader_id in range(workers):
        proc = Process(target=_reader, args=(reader_id, path_queue, item_queue, pipelines))
        readers.append(proc)
        proc.start()

    for joinable in readers + [path_queue, item_queue]:
        joinable.join()


def _reader(id, path_queue, item_queue, pipelines):
    logger_r = logger.getChild(f'readers.{id}')
    logger_r.debug(f"Starting, preprocessing pipelines: {pipelines!r}")
    pipelines = load_pipelines(pipelines)
    try:
        while True:
            path = path_queue.get(timeout=1)
            logger_r.debug(f"Parsing {path}")
            counter = 0
            for item in parse(path):
                item = execute_pipelines(item, pipelines)
                item_queue.put(item)
                counter += 1
            logger_r.info(f"Parsed {path} into {counter} items")
            path_queue.task_done()
    except Empty:
        logger_r.debug("Nothing else to parse, closing")


@db.connection_context()
def _writer(item_queue):
    logger_w = logger.getChild('writer')
    logger_w.debug("Starting")
    try:
        while True:
            item = item_queue.get()
            logger_w.debug(f"Saving {item['url']}")
            job = Job.from_item(item)
            try:
                job.save()
            except IntegrityError:
                job = Job.get_by_item(item)
                job.merge_item(item)
                job.save()
            except Exception:
                logger_w.error(f'Error saving the following item:\n{pformat(item)}')
                raise
            logger_w.debug(f"Saved {item['url']} as {job!r}")
            item_queue.task_done()
    finally:
        logger_w.debug("Closing writer")


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
        logger_p = logger.getChild('parse')
        logger_p.error(f'Error parsing the following data:\n\n{line}\n\n'
                       f'Line number: {line_no}, file: {path}')
        raise


def path_to_date(path):
    return date(year=int(path.parent.parent.parent.stem),
                month=int(path.parent.parent.stem),
                day=int(path.parent.stem))


def postprocess_jobs(pipelines, workers=None):
    workers = workers or WORKERS

    id_queue = Queue()
    Process(target=_query, args=(id_queue,), daemon=True).start()

    op_queue = Queue()
    Process(target=_persistor, args=(op_queue,), daemon=True).start()

    postprocessors = []
    for postprocessor_id in range(workers):
        proc = Process(target=_postprocessor, args=(postprocessor_id, op_queue, id_queue, pipelines))
        postprocessors.append(proc)
        proc.start()

    for joinable in postprocessors + [op_queue, id_queue]:
        joinable.join()


db.connection_context()
def _query(id_queue):
    for job in Job.select(Job.id).iterator():
        id_queue.put(job.id)


db.connection_context()
def _postprocessor(id, op_queue, id_queue, pipelines):
    logger_p = logger.getChild(f'postprocessors.{id}')
    logger_p.debug(f"Starting, preprocessing pipelines: {pipelines!r}")
    pipelines = load_pipelines(pipelines)
    try:
        while True:
            job_id = id_queue.get(timeout=1)
            job = Job.get(job_id)
            logger_p.debug(f"Executing pipelines for {job!r}")
            item = job.to_item()
            try:
                op_queue.put(('save', execute_pipelines(item, pipelines)))
            except DropItem:
                logger_p.info(f"Dropping {job!r}")
                op_queue.put(('delete', {'id': job_id}))
            id_queue.task_done()
    except Empty:
        logger_p.debug("Nothing else to postprocess, closing")


@db.connection_context()
def _persistor(op_queue):
    logger_p = logger.getChild('persistor')
    logger_p.debug("Starting")
    try:
        while True:
            operation, item = op_queue.get()
            job = Job.from_item(item)
            try:
                if operation == 'delete':
                    logger_p.debug(f"Deleting {job!r}")
                    job.delete_instance()
                elif operation == 'save':
                    logger_p.debug(f"Updating {job!r}")
                    job.save()
                else:
                    raise ValueError(f'Unknown operation: {operation}')
            except Exception:
                logger_p.error(f'Error saving the following item:\n{pformat(item)}')
                raise
            del job
            op_queue.task_done()
    finally:
        logger_p.debug("Closing persistor")


def load_pipelines(pipelines):
    return [importlib.import_module(pipeline).process
            for pipeline in pipelines]


def execute_pipelines(item, pipelines):
    for pipeline in pipelines:
        item = pipeline(item)
    return item
