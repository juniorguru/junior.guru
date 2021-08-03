import re
from pathlib import Path
from operator import attrgetter, itemgetter

import arrow

from juniorguru.models import with_db, Metric, Topic, ClubUser, Company, Event, ClubMessage
from juniorguru.web import thumbnail


CLUB_LAUNCH_AT = arrow.get(2021, 2, 1)


def on_shared_context(context, page, config, files):
    context['now'] = arrow.utcnow()


@with_db
def on_markdown_context(context, page, config, files):
    context['page'] = page
    context['config'] = config
    context['pages'] = files

    context['club_elapsed_months'] = int(round((context['now'] - CLUB_LAUNCH_AT).days / 30))
    context['members'] = ClubUser.avatars_listing()
    context['members_total_count'] = ClubUser.members_count()
    context['messages_count'] = ClubMessage.count()
    context['companies'] = Company.listing()
    context['companies_students'] = Company.students_listing()
    context['events'] = Event.listing()

    # TODO
    # if 'thumbnail_title' in page.meta:
    #     context['thumbnail'] = thumbnail(title=page.meta['thumbnail_title'])

    if 'topic_name' in page.meta:
        topic_name = page.meta['topic_name']
        context['topic'] = Topic.get_by_id(topic_name)


METRICS_INC_NAMES = {
    'inc_donations_pct': 'dobrovolné příspěvky',
    'inc_jobs_pct': 'inzerce nabídek práce',
    'inc_memberships_pct': 'individuální členství',
    'inc_partnerships_pct': 'firemní členství',
}


@with_db
def on_theme_context(context, page, config, files):
    context['page'].meta.setdefault('title', 'Jak se naučit programovat a získat první práci v IT')
    context['page'].meta.setdefault('main_class', 'main-simple')
    context['page'].meta.setdefault('thumbnail', thumbnail())

    context['nav_topics'] = sorted([
        file.page for file in files
        if file.src_path.startswith('topics/')
    ], key=attrgetter('url'))

    metrics = Metric.as_dict()
    context['metrics'] = metrics
    context['metrics_inc_breakdown'] = sorted((
        (METRICS_INC_NAMES[name], value) for name, value
        in metrics.items()
        if name.startswith('inc_') and name.endswith('_pct')
    ), key=itemgetter(1), reverse=True)

    css_path = Path(__file__).parent.parent / 'web' / 'static' / 'bundle-mkdocs.css'
    context['bootstrap_icons_file'] = re.search(r'bootstrap-icons.woff2\?\w+', css_path.read_text()).group(0)
