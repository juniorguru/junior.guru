import arrow


def on_env(env, config, files):
    env.globals.update(dict(
        now=arrow.utcnow(),
    ))
    # nav_tabs=NAV_TABS,
    # handbook_release_at=arrow.get(2020, 9, 1),
    # thumbnail=thumbnail()
