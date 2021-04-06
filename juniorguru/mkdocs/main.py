import arrow

from juniorguru.web import NAV_TABS
from juniorguru.web.thumbnail import thumbnail


def define_env(env):
    # env.conf['extra'].update(dict(
    #     now=arrow.utcnow(),
    #     nav_tabs=NAV_TABS,
    #     thumbnail=thumbnail(),
    #     handbook_release_at=arrow.get(2020, 9, 1),
    # ))
    pass


def on_pre_page_macros(env):
    env.page.meta.update(dict(
        now=arrow.utcnow(),
        nav_tabs=NAV_TABS,
        thumbnail=thumbnail(),
        handbook_release_at=arrow.get(2020, 9, 1),
    ))
