from juniorguru.lib.scrapers import scrape
from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.models import Employment, db


logger = loggers.get(__name__)


@measure()
def main():
    with db:
        db.drop_tables([Employment])
        db.create_tables([Employment])

    scrape('juniorguru.sync.employments', ['backups'])
