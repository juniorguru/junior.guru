import re
import hashlib
from pathlib import Path
from urllib.parse import urljoin

import arrow

from juniorguru.models import with_db, Metric, Topic, ClubUser, Company, Event, ClubMessage
from juniorguru.mkdocs.thumbnail import thumbnail


CLUB_LAUNCH_AT = arrow.get(2021, 2, 1)


def on_shared_context(context, page, config, files):
    context['now'] = arrow.utcnow()


@with_db
def on_docs_context(context, page, config, files):
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

    if 'topic_name' in page.meta:
        topic_name = page.meta['topic_name']
        context['topic'] = Topic.get_by_id(topic_name)


@with_db
def on_theme_context(context, page, config, files):
    context['page'].meta.setdefault('title', 'Jak se naučit programovat a získat první práci v IT')

    thumbnail_path = thumbnail(context['page'].meta.get('thumbnail_title', context['page'].meta['title']),
                               badge=context['page'].meta.get('thumbnail_badge'))
    context['thumbnail_url'] = urljoin(config['site_url'], f'static/{thumbnail_path}')

    js_path = Path(__file__).parent.parent / 'web' / 'static' / 'bundle.js'
    css_path = Path(__file__).parent.parent / 'web' / 'static' / 'bundle-mkdocs.css'
    context['js_hash'] = hash_file(js_path)
    context['css_hash'] = hash_file(css_path)
    context['bootstrap_icons_file'] = re.search(r'bootstrap-icons.woff2\?\w+', css_path.read_text()).group(0)

    context['metrics'] = Metric.as_dict()


def hash_file(path):
    hash = hashlib.sha512()
    hash.update(path.read_bytes())
    return hash.hexdigest()
