import subprocess
from multiprocessing import Pool
from pathlib import Path

from juniorguru.lib import timer
from juniorguru.models import Job, JobDropped, JobError, SpiderMetric, db
from juniorguru.scrapers.settings import IMAGES_STORE


@timer.notify
def main():
    # If the creation of the directory is left to the spiders, they can end
    # up colliding in making sure it gets created
    Path(IMAGES_STORE).mkdir(exist_ok=True, parents=True)

    with db:
        for model in [Job, JobError, JobDropped, SpiderMetric]:
            model.drop_table()
            model.create_table()

    Pool().map(run_spider, [
        'juniorguru',
        'linkedin',
        'stackoverflow',
        'startupjobs',
        'remoteok',
    ])


def run_spider(spider_name):
    return subprocess.run(['scrapy', 'crawl', spider_name], check=True)


if __name__ == '__main__':
    main()
