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

    spider_names = [
        'linkedin',
        'juniorguru',
        'stackoverflow',
        'startupjobs',
        'remoteok',
        'wwr',
    ]
    Pool().map(run_spider, spider_names)


def run_spider(spider_name):
    proc = subprocess.Popen(['scrapy', 'crawl', spider_name], text=True, bufsize=1,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        for line in proc.stdout:
            print(f'[jobs/{spider_name}] {line}', end='')
    except KeyboardInterrupt:
        proc.kill()
        proc.communicate()


if __name__ == '__main__':
    main()
