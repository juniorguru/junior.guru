import logging
from pathlib import Path

from scrapy import signals
from scrapy.exporters import JsonItemExporter


logger = logging.getLogger(__name__)


MONITORING_OUTPUT_DIR = Path('juniorguru/data/jobs')
JSON_ENCODER_OPTIONS = {'ensure_ascii': False, 'indent': 2}


class BaseMonitoring():
    def engine_started(self):
        assert self.export_path, f'{self.__class__.__name__}.export_path must be set'
        self.export_path.parent.mkdir(parents=True, exist_ok=True)
        self.file = self.export_path.open(mode='wb')
        self.exporter = JsonItemExporter(self.file, **JSON_ENCODER_OPTIONS)
        self.exporter.start_exporting()

    def engine_stopped(self):
        self.exporter.finish_exporting()
        self.file.close()


class DropMonitoring(BaseMonitoring):
    export_path = MONITORING_OUTPUT_DIR / 'drops.json'

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.engine_started, signal=signals.engine_started)
        crawler.signals.connect(ext.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(ext.engine_stopped, signal=signals.engine_stopped)
        return ext

    def item_dropped(self, item, response, exception, spider):
        item = dict(drop_type=exception.__class__.__name__,
                    drop_reason=str(exception),
                    **item)
        self.exporter.export_item(item)


class ErrorMonitoring(BaseMonitoring):
    export_path = MONITORING_OUTPUT_DIR / 'errors.json'

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.engine_started, signal=signals.engine_started)
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        crawler.signals.connect(ext.item_error, signal=signals.item_error)
        crawler.signals.connect(ext.engine_stopped, signal=signals.engine_stopped)
        return ext

    def item_error(self, item, response, spider, failure):
        item = dict(error_message=f'{failure.type.__name__}: {failure.getErrorMessage()}',
                    error_trace=failure.getTraceback(),
                    error_signal='item',
                    error_url=response.url,
                    error_spider=spider.name,
                    **item)
        self.exporter.export_item(item)

    def spider_error(self, failure, response, spider):
        item = dict(error_message=f'{failure.type.__name__}: {failure.getErrorMessage()}',
                    error_trace=failure.getTraceback(),
                    error_signal='spider',
                    error_url=response.url,
                    error_spider=spider.name)
        self.exporter.export_item(item)
