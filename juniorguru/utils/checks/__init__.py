from invoke import Collection

from juniorguru.utils.checks.docs import main as docs_task
from juniorguru.utils.checks.links import main as links_task


namespace = Collection(docs_task, links_task)
