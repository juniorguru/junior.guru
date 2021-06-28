from operator import attrgetter


def build_nav(context, page, config, nav):
    context['nav_topics'] = sorted([
        file.page for file in context['pages']
        if file.url.startswith('topics/')
    ], key=attrgetter('url'))
