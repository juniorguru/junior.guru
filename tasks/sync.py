import importlib

from invoke import task, Collection


TASKS_MODULE_PATHS = [
    'juniorguru.sync.avatars',
    'juniorguru.sync.club_content',
    'juniorguru.sync.companies',
    'juniorguru.sync.digest',
    'juniorguru.sync.events',
    'juniorguru.sync.jobs_scraped',
    'juniorguru.sync.jobs_submitted',
    'juniorguru.sync.last_modified',
    'juniorguru.sync.li_group',
    'juniorguru.sync.mentoring',
    'juniorguru.sync.pins',
    'juniorguru.sync.podcast',
    'juniorguru.sync.returning_members',
    'juniorguru.sync.roles',
    'juniorguru.sync.stickers',
    'juniorguru.sync.stories',
    'juniorguru.sync.subscriptions',
    'juniorguru.sync.supporters',
    'juniorguru.sync.topics',
    'juniorguru.sync.transactions',
]

TASKS = [importlib.import_module(module_path).main
         for module_path in TASKS_MODULE_PATHS]


@task(*TASKS, default=True)
def sync(context):
    pass


namespace = Collection(sync, *TASKS)



# @task()
# def scrapers_jobs(context):
#     context.run('python -m juniorguru.scrapers.jobs')


# @task()
# def scrapers_companies(context):
#     context.run('python -m juniorguru.scrapers.companies')


# scrapers-jobs:
# 	poetry run python -m juniorguru.scrapers.jobs

# scrapers-companies:
# 	poetry run python -m juniorguru.scrapers.companies

