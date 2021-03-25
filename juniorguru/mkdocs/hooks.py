import arrow

from juniorguru.web import NAV_TABS
from juniorguru.web.thumbnail import thumbnail


def on_env(env, config, files):
    env.globals.update(dict(
        now=arrow.utcnow(),
        nav_tabs=NAV_TABS,
        thumbnail=thumbnail(),
        handbook_release_at=arrow.get(2020, 9, 1),
    ))
