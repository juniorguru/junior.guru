from typing import Any

from peewee import CharField

from juniorguru.models.base import BaseModel, JSONField


class Chart(BaseModel):
    slug = CharField()
    labels = JSONField(null=True)
    data = JSONField()
    annotations = JSONField(null=True)

    @classmethod
    def as_dict(cls) -> dict[str, list[Any]]:
        charts = {}
        for chart in cls.select():
            charts[chart.slug] = chart.data
            if chart.labels is not None:
                charts[f'{chart.slug}_labels'] = chart.labels
            if chart.annotations is not None:
                charts[f'{chart.slug}_annotations'] = chart.annotations
        return charts
