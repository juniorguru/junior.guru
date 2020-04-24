import logging
from pathlib import Path

from scrapy import signals
from scrapy.exporters import JsonItemExporter


logger = logging.getLogger(__name__)


class Monitoring():
    output_dir = 'juniorguru/data/jobs/'
    json_encoder_kwargs = {'ensure_ascii': False, 'indent': 2}

    def __init__(self):
        self.path_dropped = Path(self.output_dir) / 'dropped.json'

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.engine_started, signal=signals.engine_started)
        crawler.signals.connect(ext.item_dropped, signal=signals.item_dropped)
        # crawler.signals.connect(ext.item_error, signal=signals.item_error)
        crawler.signals.connect(ext.engine_stopped, signal=signals.engine_stopped)
        return ext

    def engine_started(self):
        self.path_dropped.parent.mkdir(parents=True, exist_ok=True)
        self.file = self.path_dropped.open(mode='wb')
        self.exporter_dropped = JsonItemExporter(self.file, **self.json_encoder_kwargs)
        self.exporter_dropped.start_exporting()

    def item_dropped(self, item, response, exception, spider):
        item = dict(item)
        item['drop_type'] = exception.__class__.__name__
        item['drop_reason'] = str(exception)
        self.exporter_dropped.export_item(item)

#         logger.error('''
# *******************************************************************************
# ITEM DROPPED OMG OMG
# *******************************************************************************
#         ''', extra={'spider': spider})


#     def item_error(self, item, response, spider, failure):
#         logger.error('''
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ERROR OMG OMG
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#         ''', extra={'spider': spider})

    def engine_stopped(self):
        self.exporter_dropped.finish_exporting()
        self.file.close()
