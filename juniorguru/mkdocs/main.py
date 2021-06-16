import random

import arrow
import mkdocs_macros

from juniorguru.web import NAV_TABS, thumbnail
from juniorguru.models import db, Topic, ClubUser


def define_env(env):
    with db:
        env.variables.update(dict(
            members=ClubUser.avatars_listing(),
            members_total_count=ClubUser.members_count(),
        ))

    @env.filter
    def url(path):  # mimicking the built-in MkDocs' url() filter
        return mkdocs_macros.fix_url(f'../{path}')

    @env.filter
    def sample(items, n=2, sample_fn=None):  # TODO deduplicate template_filters
        items = list(items)
        if len(items) <= n:
            return items
        return (sample_fn or random.sample)(items, n)


def on_pre_page_macros(env):
    now = arrow.utcnow()
    club_launch_at = arrow.get(2021, 2, 1)

    env.page.meta.setdefault('title', 'Jak se naučit programovat a získat první práci v IT')
    env.page.meta.update(dict(
        now=now,
        nav_tabs=NAV_TABS,
        thumbnail=thumbnail(),
        handbook_release_at=arrow.get(2020, 9, 1),
        club_launch_at=club_launch_at,
        club_elapsed_months=int(round((now - club_launch_at).days / 30)),
    ))

    try:
        topic_name = env.page.meta['topic_name']
    except KeyError:
        pass
    else:
        with db:
            env.page.meta['topic'] = Topic.get_by_id(topic_name)


# TODO @on_meta_key('messages_topic')
