import importlib
import os
from pathlib import Path
from queue import Empty
from multiprocessing import Process, JoinableQueue as Queue, Pool
import json
from datetime import date

from pprint import pformat
from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict, dict_to_model

from juniorguru.lib import loggers
from juniorguru.models import db, with_db, Job


logger = loggers.get('juniorguru.sync.jobs')


WORKERS = os.cpu_count()


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
    logger_r.debug("Starting")
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


def _writer(item_queue):
    logger_w = logger.getChild('writer')
    logger_w.debug("Starting")
    try:
        while True:
            item = item_queue.get()
            logger_w.debug(f"Saving {item['url']}")
            with db:
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


@with_db
def postprocess_jobs(pipelines, workers=None):
    workers = workers or WORKERS

    logger_p = logger.getChild('postprocess')
    logger_p.info('Postprocessing jobs')

    jobs = Job.select(Job.id)
    args_generator = ((job.id, pipelines) for job in jobs)

    # The following code can be heavy on memory. The 'chunksize' makes it more
    # efficient as well as using 'while' instead of 'for in', because this way
    # it's possible to micromanage the lifecycle of the 'job' variable and clear
    # it from memory as soon as its contents are not needed. Also the job itself
    # is transferred between processes as a dict (efficient), not as a 'Job'
    # instance (convoluted).

    with Pool(workers) as pool:
        jobs = pool.imap_unordered(_processor, args_generator, chunksize=10)
        while True:
            try:
                job = dict_to_model(Job, next(jobs))
                logger_p.debug(f'Updating {job!r}')
                job.save()
                del job
            except StopIteration:
                break


def _processor(args):
    job_id, pipelines = args

    job = Job.get(job_id)
    pipelines = load_pipelines(pipelines)

    logger_p = logger.getChild('postprocess')
    logger_p.debug(f'Executing pipelines for {job!r}')

    return model_to_dict(execute_pipelines(job, pipelines))


def load_pipelines(pipelines):
    return [importlib.import_module(pipeline).process
            for pipeline in pipelines]


def execute_pipelines(item_or_job, pipelines):
    return item_or_job  # TODO
