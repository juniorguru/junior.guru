import os
import importlib
import subprocess
from multiprocessing import Pool


def run(scrapy_project_package, spider_name):
    settings_module_name = f'{scrapy_project_package}.settings'
    settings = importlib.import_module(settings_module_name)

    env = dict(**os.environ)
    env['SCRAPY_SETTINGS_MODULE'] = settings_module_name

    proc = subprocess.Popen(['scrapy', 'crawl', spider_name], text=True, bufsize=1, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        for line in proc.stdout:
            print(f'[{settings.BOT_NAME}/{spider_name}] {line}', end='')
    except KeyboardInterrupt:
        proc.kill()
        proc.communicate()


def run_many(scrapy_project_package, spider_names):
    args = ((scrapy_project_package, spider_name) for spider_name in spider_names)
    Pool().starmap(run, args)
