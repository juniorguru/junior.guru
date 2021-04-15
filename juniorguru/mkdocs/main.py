import random

import arrow

from juniorguru.web import NAV_TABS
from juniorguru.web.thumbnail import thumbnail
from juniorguru.models import db, Topic, Member, Job


def define_env(env):
    with db:
        env.variables.update(dict(
            members=Member.avatars_listing(),
            members_total_count=Member.count(),
            jobs_count=Job.aggregate_metrics()['jobs_count'],
        ))

    @env.filter
    def sample(items, n=2, sample_fn=None):  # TODO deduplicate template_filters
        items = list(items)
        if len(items) <= n:
            return items
        return (sample_fn or random.sample)(items, n)


def on_pre_page_macros(env):
    env.page.meta.update(dict(
        now=arrow.utcnow(),
        nav_tabs=NAV_TABS,
        thumbnail=thumbnail(),
        handbook_release_at=arrow.get(2020, 9, 1),
    ))

    try:
        topic_name = env.page.meta['topic_name']
    except KeyError:
        pass
    else:
        with db:
            env.page.meta['topic'] = Topic.get_by_id(topic_name)


# TODO @on_meta_key('messages_topic')
