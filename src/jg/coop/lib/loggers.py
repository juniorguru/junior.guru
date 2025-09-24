import logging
import os
import threading
import time
from pathlib import Path
from typing import Callable, Generator, Iterable, TypeVar, cast

import click

from jg.coop.lib.cache import get_cache
from jg.coop.lib.chunks import chunks


T = TypeVar("T")

MUTED_LOGGERS = [
    "asyncio",
    "discord",
    "google",
    "googleapiclient",
    "gql.transport.requests",
    "httpcore",
    "httpx",
    "jg.coop.lib.mutations.allowing",
    "jg.coop.sync.club_content.store",
    "jg.coop.web.templates",
    "MARKDOWN",
    "oauth2client",
    "openai._base_client",
    "peewee",
    "PIL",
    "protego",
    "stripe",
    "tornado.access",
    "urllib3",
]

CACHE_TAG = "loggers"


class Logger(logging.Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configured = False

    def __getitem__(self, name) -> logging.Logger:
        return self.getChild(str(name))

    def progress(
        self, iterable: Iterable[T], chunk_size=100
    ) -> Generator[T, None, None]:
        total_count = 0
        for chunk in chunks(iterable, size=chunk_size):
            yield from chunk
            total_count += len(chunk)
            self.info(f"Done {total_count} items")

    def wait(self, fn: Callable[..., T], *args, **kwargs) -> T:
        stop = False

        def wait() -> None:
            t = time.perf_counter()
            time.sleep(3)
            while not stop:
                self.info(f"Waiting… ({(time.perf_counter() - t) / 60:.0f}min)")
                time.sleep(60)

        thread = threading.Thread(target=wait)
        thread.start()
        try:
            return fn(*args, **kwargs)
        finally:
            stop = True
            thread.join()


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if record.levelno == logging.DEBUG:
            record.levelname = click.style("DEBUG", fg="cyan")
        elif record.levelno == logging.INFO:
            record.levelname = click.style("INFO", fg="green")
        elif record.levelno == logging.WARNING:
            record.levelname = click.style("WARNING", fg="yellow")
        elif record.levelno == logging.ERROR:
            record.levelname = click.style("ERROR", fg="red")
        elif record.levelno == logging.CRITICAL:
            record.levelname = click.style("CRITICAL", fg="red")
        return super().format(record)


def _configure():
    cache = get_cache()

    level = _infer_level(cache.get("loggers:log_level"), os.environ)
    timestamp = _infer_timestamp(cache.get("loggers:log_timestamp"), os.environ)
    format = "[%(asctime)s] " if timestamp else ""
    format += "[%(name)s%(processSuffix)s] %(levelname)s %(message)s"

    logging.setLogRecordFactory(_record_factory)
    logging.setLoggerClass(Logger)
    logging.root.setLevel(logging.DEBUG)

    for name in MUTED_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

    stderr = logging.StreamHandler()
    stderr.setLevel(getattr(logging, level))
    stderr.setFormatter(ColorFormatter(format))
    logging.root.addHandler(stderr)

    # In multiprocessing, the child processes won't automatically
    # inherit logger configuration and this function will run again.
    cache.set("loggers:log_level", level, tag=CACHE_TAG)
    cache.set("loggers:log_timestamp", timestamp, tag=CACHE_TAG)

    logging.root.configured = True


def reconfigure_level(level: str):
    for handler in logging.root.handlers:
        handler.setLevel(getattr(logging, level.upper()))
    get_cache().set("loggers:log_level", level, tag=CACHE_TAG)


def clear_configuration():
    try:
        get_cache().evict(CACHE_TAG)
    except Exception as e:
        logger = logging.getLogger("jg.coop.lib.loggers")
        logger.warning(f"Failed to clear loggers configuration: {e}")


_original_record_factory = logging.getLogRecordFactory()


def _record_factory(*args, **kwargs) -> logging.LogRecord:
    record = _original_record_factory(*args, **kwargs)
    record.processSuffix = _get_process_suffix(record.processName)
    return record


def _get_process_suffix(process_name: str) -> str:
    return (
        process_name.replace("MainProcess", "")
        .replace("SpawnPoolWorker-", "/worker")
        .replace("ForkPoolWorker-", "/worker")
        .replace("Process-", "/process")
    )


def _infer_level(cached_value: str | None, env: dict) -> str:
    value = cached_value
    if value is None:
        value = env.get("LOG_LEVEL")
    if not value:
        return "INFO"
    return value.upper()


def _infer_timestamp(cached_value: bool | None, env: dict) -> bool:
    value = cached_value
    if value is None:
        value = env.get("LOG_TIMESTAMP")
    if value is None:
        value = env.get("CI")
    if not value or value.lower() in ["0", "false"]:
        return False
    return True


def get(name) -> Logger:
    return cast(Logger, logging.getLogger(name))


def from_path(path, cwd=None) -> Logger:
    cwd = cwd or os.getcwd()
    relative_path = str(Path(path).relative_to(cwd))
    name = ".".join(
        relative_path.removesuffix(".py")
        .removesuffix("__init__")
        .rstrip("/")
        .split("/")
    )
    return get(name)


if not getattr(logging.root, "configured", False):
    _configure()
