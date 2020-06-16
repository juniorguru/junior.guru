from juniorguru.models.base import db
from juniorguru.models.job import Job, JobDropped, JobError
from juniorguru.models.metrics import GlobalMetric, JobMetric
from juniorguru.models.story import Story
from juniorguru.models.supporter import Supporter


# This is here because of circular dependencies between Job and JobMetric
# https://stackoverflow.com/q/62327182/325365

from juniorguru.models import job_attrs  # isort:skip

for attr_name in job_attrs.__all__:
    setattr(Job, attr_name, getattr(job_attrs, attr_name))
