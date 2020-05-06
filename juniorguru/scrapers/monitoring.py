import hashlib
import logging
import re
from pathlib import Path
from urllib.parse import urlparse

from scrapy import signals

from juniorguru.models import Job, JobDropped, JobError, db
from juniorguru.scrapers.pipelines.database import item_to_job_id


logger = logging.getLogger(__name__)


RESPONSES_BACKUP_DIR = Path('juniorguru/data/responses/').absolute()


class BackupResponseMiddleware():
    def process_response(self, request, response, spider):
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


class MonitoringExtension():
    def __init__(self, stats=None):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(stats=crawler.stats)
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        crawler.signals.connect(ext.item_error, signal=signals.item_error)
        crawler.signals.connect(ext.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        return ext

    def spider_error(self, failure, response, spider):
        with db:
            JobError.create(message=get_failure_message(failure),
                            trace=failure.getTraceback(),
                            signal='spider',
                            spider=spider.name,
                            response_url=response.url,
                            response_backup_path=get_response_backup_path(response.url))
        if self.stats:
            self.stats.inc_value('monitoring/job_error_saved')

    def item_error(self, item, response, spider, failure):
        with db:
            JobError.create(message=get_failure_message(failure),
                            trace=failure.getTraceback(),
                            signal='item',
                            spider=spider.name,
                            response_url=response.url,
                            response_backup_path=get_response_backup_path(response.url),
                            item=item)
        if self.stats:
            self.stats.inc_value('monitoring/job_error_saved')

    def item_dropped(self, item, response, exception, spider):
        with db:
            JobDropped.create(type=exception.__class__.__name__,
                              reason=str(exception),
                              response_url=response.url,
                              response_backup_path=get_response_backup_path(response.url),
                              item=item)
        if self.stats:
            self.stats.inc_value('monitoring/job_dropped_saved')

    def item_scraped(self, item, response, spider):
        with db:
            job = Job.get_by_id(item_to_job_id(item))
            job.response_url = response.url
            job.response_backup_path = get_response_backup_path(response.url)
            job.item = item
            job.save()
            logger.debug(f"Updated job '{job.id}' with monitoring data")
        if self.stats:
            self.stats.inc_value('monitoring/job_saved')


def url_to_backup_path(url):
    path = RESPONSES_BACKUP_DIR / urlparse(url).hostname
    return path / f'{hashlib.sha224(url.encode()).hexdigest()}.txt'


def get_response_backup_path(url):
    return url_to_backup_path(url).relative_to(RESPONSES_BACKUP_DIR)


def get_failure_message(failure):
    return f'{failure.type.__name__}: {failure.getErrorMessage()}'
