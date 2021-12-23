import re
import hashlib
from pathlib import Path
from urllib.parse import urljoin

import arrow

from juniorguru.lib import charts
from juniorguru.models import with_db, Metric, Topic, ClubUser, Company, Event, ClubMessage, Story, LastModified, Job, Transaction
from juniorguru.mkdocs.thumbnail import thumbnail


CLUB_LAUNCH_AT = arrow.get(2021, 2, 1)


def on_shared_context(context, page, config, files):
    context['now'] = arrow.utcnow()
    context['pricing_url'] = 'https://docs.google.com/document/d/1keFyO5aavfaNfJkKlyYha4B-UbdnMja6AhprS_76E7c/'
    context['transactions'] = Transaction


@with_db
def on_docs_context(context, page, config, files):
    context['club_elapsed_months'] = int(round((context['now'] - CLUB_LAUNCH_AT).days / 30))
    context['members'] = ClubUser.avatars_listing()
    context['members_total_count'] = ClubUser.members_count()
    context['messages_count'] = ClubMessage.count()
    context['companies'] = Company.listing()
    context['companies_students'] = Company.students_listing()
    context['events'] = Event.listing()
    context['stories'] = Story.listing()
    context['stories_by_tags'] = Story.tags_mapping()
    context['last_modified'] = LastModified.get_value_by_path('candidate-handbook.md')
    context['jobs'] = Job.listing()
    context['jobs_remote'] = Job.remote_listing()
    context['jobs_internship'] = Job.internship_listing()
    context['jobs_volunteering'] = Job.volunteering_listing()
    context['charts_ranges'] = charts.ranges(context['now'].date())

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

    context['parent_page'] = get_parent_page(context['page'])
    context['previous_page'] = get_sibling_page(context['page'], -1)
    context['next_page'] = get_sibling_page(context['page'], +1)

    context['metrics'] = Metric.as_dict()
    context['companies_handbook'] = Company.handbook_listing()


def hash_file(path):
    hash = hashlib.sha512()
    hash.update(path.read_bytes())
    return hash.hexdigest()


def get_parent_page(page):
    try:
        return page.parent.children[0]
    except AttributeError:
        return None


def get_sibling_page(page, offset):
    try:
        index = page.parent.children.index(page)
        sibling_index = max(index + offset, 0)
        if index == sibling_index:
            return None
        return page.parent.children[sibling_index]
    except (AttributeError, IndexError):
        return None
