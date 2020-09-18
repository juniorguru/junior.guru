import hashlib
import logging
import time
from functools import wraps
from pathlib import Path
from urllib.parse import urlparse

from peewee import OperationalError
from scrapy import signals

from juniorguru.models import Job, JobDropped, JobError, db
from juniorguru.scrapers.pipelines.database import create_id


logger = logging.getLogger(__name__)


RESPONSES_BACKUP_DIR = Path('juniorguru/data/responses/').absolute()


class BackupResponseMiddleware():
    def process_response(self, request, response, spider):
        if hasattr(spider, 'override_response_backup_path'):
            logger.debug(f"Skipping backup of '{response.url}' per spider override")
        else:
            try:
                response_text = response.text
            except AttributeError:
                logger.debug(f"Unable to backup '{response.url}'")
            else:
                path = url_to_backup_path(response.url)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(response_text)
                logger.debug(f"Backed up '{response.url}' as '{path.absolute()}'")
        return response


def retry_when_db_locked(method):
    @wraps(method)
    def wrapper(ext, *args, **kwargs):
        kwargs.pop('signal')
        kwargs.pop('sender')
        last_error = None
        for i in range(5):
            try:
                return method(ext, *args, **kwargs)
            except OperationalError as error:
                if str(error) == 'database is locked':
                    logger.debug(f"Monitoring operation '{method.__name__}' failed! ({error}, attempt: {i + 1})")
                    last_error = error
                    ext.stats.inc_value('monitoring/db_locked_retries')
                    time.sleep(0.5)
                else:
                    ext.stats.inc_value('monitoring/uncaught_errors')
                    raise
        ext.stats.inc_value('monitoring/uncaught_errors')
        raise last_error
    return wrapper


class MonitoringExtension():
    def __init__(self, stats):
        self.stats = stats
        self.postponed_operations = []

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        crawler.signals.connect(ext.item_error, signal=signals.item_error)
        crawler.signals.connect(ext.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        return ext

    @retry_when_db_locked
    def spider_error(self, failure, response, spider):
        response_data = get_response_data(spider, response.url)
        with db:
            JobError.create(message=get_failure_message(failure),
                            trace=failure.getTraceback(),
                            signal='spider',
                            spider=spider.name,
                            **response_data)
        self.stats.inc_value('monitoring/job_error_saved')

    @retry_when_db_locked
    def item_error(self, item, response, spider, failure):
        response_data = get_response_data(spider, response.url)
        with db:
            JobError.create(message=get_failure_message(failure),
                            trace=failure.getTraceback(),
                            signal='item',
                            spider=spider.name,
                            item=item,
                            **response_data)
        self.stats.inc_value('monitoring/job_error_saved')

    @retry_when_db_locked
    def item_dropped(self, item, response, exception, spider):
        response_data = get_response_data(spider, response.url)
        with db:
            JobDropped.create(type=exception.__class__.__name__,
                              reason=str(exception),
                              item=item,
                              **response_data)
        self.stats.inc_value('monitoring/job_dropped_saved')

    @retry_when_db_locked
    def item_scraped(self, item, response, spider):
        response_data = get_response_data(spider, response.url)
        with db:
            job = Job.get_by_id(item.get('id', create_id(item)))
            job.item = item
            for attr, value in response_data.items():
                setattr(job, attr, value)
            job.save()
            logger.debug(f"Updated job '{job.id}' with monitoring data")
        self.stats.inc_value('monitoring/job_saved')


def get_response_data(spider, response_url):
    data = {}
    try:
        data['response_url'] = spider.override_response_url
    except AttributeError:
        data['response_url'] = response_url
    try:
        data['response_backup_path'] = spider.override_response_backup_path
    except AttributeError:
        data['response_backup_path'] = get_response_backup_path(response_url)
    return data


def url_to_backup_path(url):
    path = RESPONSES_BACKUP_DIR / urlparse(url).hostname
    return path / f'{hashlib.sha224(url.encode()).hexdigest()}.txt'


def get_response_backup_path(url):
    return url_to_backup_path(url).relative_to(RESPONSES_BACKUP_DIR)


def get_failure_message(failure):
    return f'{failure.type.__name__}: {failure.getErrorMessage()}'
