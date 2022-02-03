import hashlib
from pathlib import Path
from urllib.parse import urlparse

from scrapy import signals

from juniorguru.lib import loggers
from juniorguru.models import Job, JobDropped, JobError, SpiderMetric, db, retry_when_db_locked


logger = loggers.get(__name__)


RESPONSES_BACKUP_DIR = Path('juniorguru/data/responses/').absolute()
RELEVANT_METRICS = (
    'database',
    'downloader/request_count',
    'downloader/response_count',
    'downloader/response_status_count',
    'log_count/ERROR',
    'item_saved_count',
    'item_dropped_count',
    'item_dropped_reasons_count',
    'item_geocoded_count',
    'elapsed_time_seconds',
)


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
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_error(self, failure, response, spider):
        response_data = get_response_data(spider, response.url)

        def operation():
            JobError.create(message=get_failure_message(failure),
                            trace=failure.getTraceback(),
                            signal='spider',
                            source=spider.name,
                            **response_data)
            self.stats.inc_value('monitoring/job_error_saved')
        retry_when_db_locked(db, operation, stats=self.stats)

    def item_error(self, item, response, spider, failure):
        response_data = get_response_data(spider, response.url)

        def operation():
            JobError.create(message=get_failure_message(failure),
                            trace=failure.getTraceback(),
                            signal='item',
                            source=spider.name,
                            item=item,
                            **response_data)
            self.stats.inc_value('monitoring/job_error_saved')
        retry_when_db_locked(db, operation, stats=self.stats)

    def item_dropped(self, item, response, exception, spider):
        response_data = get_response_data(spider, response.url)

        def operation():
            JobDropped.create(type=exception.__class__.__name__,
                              reason=str(exception),
                              item=item,
                              source=spider.name,
                              **response_data)
            self.stats.inc_value('monitoring/job_dropped_saved')
        retry_when_db_locked(db, operation, stats=self.stats)

    def item_scraped(self, item, response, spider):
        response_data = get_response_data(spider, response.url)

        def operation():
            job = Job.get_by_id(item['id'])
            job.item = item
            for attr, value in response_data.items():
                setattr(job, attr, value)
            job.save()
            logger.debug(f"Updated job '{job.id}' with monitoring data")
            self.stats.inc_value('monitoring/job_saved')
        retry_when_db_locked(db, operation, stats=self.stats)

    def spider_closed(self, spider):
        for name, value in self.stats.get_stats().items():
            if name.startswith(RELEVANT_METRICS):
                try:
                    value = int(value)
                except (TypeError, ValueError):
                    pass
                else:
                    def operation():
                        SpiderMetric.create(name=name,
                                            spider_name=spider.name,
                                            value=value)
                    retry_when_db_locked(db, operation, stats=self.stats)
        logger.debug(f"Saved '{spider.name}' spider metrics")


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
