import subprocess
from multiprocessing import Pool

from juniorguru.lib import timer
from juniorguru.models import Job, JobDropped, JobError, db


@timer.notify
def main():
    with db:
        for model in [Job, JobError, JobDropped]:
            model.drop_table()
            model.create_table()

    Pool().map(run_spider, [
        'juniorguru',
        'linkedin',
        'stackoverflow',
        'startupjobs',
    ])


def run_spider(spider_name):
    return subprocess.run(['scrapy', 'crawl', spider_name], check=True)


if __name__ == '__main__':
    main()
