from juniorguru.lib import scrapers
from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.models import Employment, db


logger = loggers.get('employments')


@measure('employments')
def main():
    with db:
        db.drop_tables([Employment])
        db.create_tables([Employment])
    scrapers.run('juniorguru.sync.employments', 'backups')
