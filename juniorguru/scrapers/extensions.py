import logging
from pathlib import Path
import hashlib
from urllib.parse import urlparse

from scrapy import signals
from scrapy.exporters import JsonItemExporter


logger = logging.getLogger(__name__)


class BaseMonitoring():
    def __init__(self, export_dir):
        assert self.export_name, f'{self.__class__.__name__}.export_name must be set'
        self.export_dir = Path(export_dir)
        self.export_path = self.export_dir / f'{self.export_name}.json'

    def engine_started(self):
        self.export_path.parent.mkdir(parents=True, exist_ok=True)
        self.file = self.export_path.open(mode='wb')
        self.exporter = JsonItemExporter(self.file, ensure_ascii=False, indent=2)
        self.exporter.start_exporting()

    def engine_stopped(self):
        self.exporter.finish_exporting()
        self.file.close()

    def backup_html(self, response):
        url = response.url
        try:
            response_text = response.text
        except AttributeError:
            logger.debug(f"Unable to backup '{url}'")
            return None

        path = self.export_dir / self.export_name / urlparse(url).hostname
        path.mkdir(parents=True, exist_ok=True)
        path = path / f'{hashlib.sha224(url.encode()).hexdigest()}.html'
        path.write_text(response_text)
        logger.debug(f"Backed up '{url}' as '{path.absolute()}'")
        return str(path.relative_to(self.export_dir))


class ErrorMonitoring(BaseMonitoring):
    export_name = 'errors'

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.settings['MONITORING_EXPORT_DIR'])
        crawler.signals.connect(ext.engine_started, signal=signals.engine_started)
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        crawler.signals.connect(ext.item_error, signal=signals.item_error)
        crawler.signals.connect(ext.engine_stopped, signal=signals.engine_stopped)
        return ext

    def item_error(self, item, response, spider, failure):
        item = dict(error_message=f'{failure.type.__name__}: {failure.getErrorMessage()}',
                    error_trace=failure.getTraceback(),
                    error_html=self.backup_html(response),
                    error_signal='item',
                    error_url=response.url,
                    error_spider=spider.name,
                    **item)
        self.exporter.export_item(item)

    def spider_error(self, failure, response, spider):
        item = dict(error_message=f'{failure.type.__name__}: {failure.getErrorMessage()}',
                    error_trace=failure.getTraceback(),
                    error_html=self.backup_html(response),
                    error_signal='spider',
                    error_url=response.url,
                    error_spider=spider.name)
        self.exporter.export_item(item)


class DropMonitoring(BaseMonitoring):
    export_name = 'drops'

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.settings['MONITORING_EXPORT_DIR'])
        crawler.signals.connect(ext.engine_started, signal=signals.engine_started)
        crawler.signals.connect(ext.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(ext.engine_stopped, signal=signals.engine_stopped)
        return ext

    def item_dropped(self, item, response, exception, spider):
        item = dict(drop_type=exception.__class__.__name__,
                    drop_reason=str(exception),
                    drop_html=self.backup_html(response),
                    **item)
        self.exporter.export_item(item)


class ItemMonitoring(BaseMonitoring):
    export_name = 'items'

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.settings['MONITORING_EXPORT_DIR'])
        crawler.signals.connect(ext.engine_started, signal=signals.engine_started)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(ext.engine_stopped, signal=signals.engine_stopped)
        return ext

    def item_scraped(self, item, response, spider):
        item = dict(html=self.backup_html(response),
                    **item)
        self.exporter.export_item(item)
