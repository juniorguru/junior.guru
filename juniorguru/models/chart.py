from typing import Any

from peewee import CharField, ForeignKeyField

from juniorguru.models.base import BaseModel, JSONField


class ChartNamespace(BaseModel):
    slug = CharField(unique=True)
    labels = JSONField(null=True)
    annotations = JSONField(null=True)


class Chart(BaseModel):
    namespace = ForeignKeyField(ChartNamespace, backref='list_charts')
    slug = CharField()
    data = JSONField()


def charts_as_dict() -> dict[str, list[Any]]:
    charts = {}
    for namespace in ChartNamespace.select():
        if namespace.labels is not None:
            charts[f'{namespace.slug}_labels'] = namespace.labels
        if namespace.annotations is not None:
            charts[f'{namespace.slug}_annotations'] = namespace.annotations
        for chart in namespace.list_charts:
            charts[f'{namespace.slug}_{chart.slug}'] = chart.data
    return charts
