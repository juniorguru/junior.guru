from invoke import task, Collection

from juniorguru.lib.tasks import import_sync_tasks


SYNC_TASKS_SCRAPE_JOBS = import_sync_tasks([
    'juniorguru.sync.proxies',
    'juniorguru.sync.scrape_jobs',
])

SYNC_TASKS_MAIN = import_sync_tasks([
    'juniorguru.sync.avatars',
    'juniorguru.sync.club_content',
    'juniorguru.sync.companies',
    'juniorguru.sync.digest',
    'juniorguru.sync.events',
    'juniorguru.sync.jobs_scraped',  # reads cached jobs data
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
])

SYNC_TASKS_POSTPROCESS_JOBS = import_sync_tasks([
    'juniorguru.sync.jobs_scraped',  # reuses db from main, adds newly scraped jobs data
    'juniorguru.sync.jobs_listing',
    'juniorguru.sync.jobs_locations',
    'juniorguru.sync.jobs_logos',
    'juniorguru.sync.jobs_emails',
    'juniorguru.sync.jobs_club',
])

SYNC_TASKS_ALL = (
    SYNC_TASKS_SCRAPE_JOBS +
    SYNC_TASKS_MAIN +
    SYNC_TASKS_POSTPROCESS_JOBS
)


@task(*SYNC_TASKS_ALL, default=True)
def sync(context):
    pass


@task(*SYNC_TASKS_SCRAPE_JOBS, name='scrape-jobs')
def ci_scrape_jobs(context):
    pass


@task(*SYNC_TASKS_MAIN, name='main')
def ci_main(context):
    pass


@task(*SYNC_TASKS_POSTPROCESS_JOBS, name='postprocess-jobs')
def ci_postprocess_jobs(context):
    pass


namespace_ci = Collection('ci', ci_scrape_jobs, ci_main, ci_postprocess_jobs)
namespace = Collection(sync, namespace_ci, *SYNC_TASKS_ALL)
