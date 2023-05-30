from itertools import groupby
from operator import attrgetter

from peewee import CharField, IntegerField

from juniorguru.models.base import BaseModel


RELEVANT_METRICS = (
    'downloader/response_status_count',
    'log_count/ERROR',
    'database',
    'item_saved_count',
    'item_dropped_count',
    'item_dropped_reasons_count',
    'elapsed_time_seconds',
)


class SpiderMetric(BaseModel):
    spider_name = CharField()
    name = CharField(index=True)
    value = IntegerField()

    @classmethod
    def as_dict(cls):
        spider_names = [sm.spider_name for sm
                        in cls.select(cls.spider_name).distinct().order_by(cls.spider_name)]
        d = {}
        for name, metrics_list in groupby(cls.select().order_by(cls.name, cls.spider_name),
                                     key=attrgetter('name')):
            if name.startswith(RELEVANT_METRICS):
                metrics_dict = {metric.spider_name: metric.value
                                for metric in metrics_list}
                d[name] = {spider_name: metrics_dict.get(spider_name, 0)
                           for spider_name in spider_names}
        return d
