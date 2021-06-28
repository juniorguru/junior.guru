from operator import attrgetter, itemgetter

from juniorguru.models import db, Metric


METRICS_INC_NAMES = {
    'inc_donations_pct': 'dobrovolné příspěvky',
    'inc_jobs_pct': 'inzerce nabídek práce',
    'inc_memberships_pct': 'individuální členství',
    'inc_partnerships_pct': 'firemní členství',
}


def on_page_context(context, page, config, nav):
    context['nav_topics'] = sorted([
        file.page for file in context['pages']
        if file.url.startswith('topics/')
    ], key=attrgetter('url'))

    with db:
        metrics = Metric.as_dict()

    context['metrics'] = metrics
    context['metrics_inc_breakdown'] = sorted((
        (METRICS_INC_NAMES[name], value) for name, value
        in metrics.items()
        if name.startswith('inc_') and name.endswith('_pct')
    ), key=itemgetter(1), reverse=True)
