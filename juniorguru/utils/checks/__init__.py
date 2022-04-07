from invoke import Collection

from juniorguru.utils.checks.anchors import main as anchors_task
from juniorguru.utils.checks.links import main as links_task


namespace = Collection(anchors_task, links_task)
