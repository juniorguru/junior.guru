from pathlib import Path
from operator import attrgetter, itemgetter

import jinja2
import arrow
from mkdocs.utils.filters import tojson
from mkdocs.utils import normalize_url, get_relative_url

from juniorguru.models import with_db, Metric, Topic, ClubUser
from juniorguru.lib import template_filters
from juniorguru.web import thumbnail


METRICS_INC_NAMES = {
    'inc_donations_pct': 'dobrovolné příspěvky',
    'inc_jobs_pct': 'inzerce nabídek práce',
    'inc_memberships_pct': 'individuální členství',
    'inc_partnerships_pct': 'firemní členství',
}


class MarkdownTemplateError(Exception):
    pass


@with_db
def on_page_markdown(markdown, page, config, files):
    """Renders Markdown as if it was a Jinja2 template.

    Inspired by https://github.com/fralau/mkdocs_macros_plugin
    """
    macros_dir = Path(config['docs_dir']).parent / 'macros'
    loader = jinja2.FileSystemLoader(macros_dir)
    env = jinja2.Environment(loader=loader, auto_reload=False)

    # prepare the url filter
    def url(value):
        return normalize_url(value, page=page, base=get_relative_url('.', page.url))

    # attach filters and tests
    env.filters.update(dict(
        # MkDocs builtin
        tojson=tojson,
        url=url,

        # custom
        email_link=template_filters.email_link,
        sample=template_filters.sample,
    ))

    # setup the md's template context
    now = arrow.utcnow()
    club_launch_at = arrow.get(2021, 2, 1)
    context = dict(now=now,
                   page=page,
                   club_elapsed_months=int(round((now - club_launch_at).days / 30)),
                   members=ClubUser.avatars_listing(),
                   members_total_count=ClubUser.members_count())

    # TODO @on_meta_key('topic_name')
    try:
        topic_name = context['page'].meta['topic_name']
    except KeyError:
        pass
    else:
        context['topic'] = Topic.get_by_id(topic_name)

    # render md as if it was jinja2
    try:
        template = env.from_string(markdown)
        return template.render(**context)
    except Exception:
        raise MarkdownTemplateError(page)


def on_env(env, config, files):
    """Enhances the theme's Jinja2 environment."""
    # attach additional filters and tests
    env.filters.update({
        'email_link': template_filters.email_link,
    })


@with_db
def on_page_context(context, page, config, nav):
    """Enhances the theme's template context."""
    context['page'].meta.setdefault('title', 'Jak se naučit programovat a získat první práci v IT')

    context['now'] = arrow.utcnow()
    context['thumbnail'] = thumbnail()
    context['nav_topics'] = sorted([
        file.page for file in context['pages']
        if file.url.startswith('topics/')
    ], key=attrgetter('url'))

    metrics = Metric.as_dict()
    context['metrics'] = metrics
    context['metrics_inc_breakdown'] = sorted((
        (METRICS_INC_NAMES[name], value) for name, value
        in metrics.items()
        if name.startswith('inc_') and name.endswith('_pct')
    ), key=itemgetter(1), reverse=True)
