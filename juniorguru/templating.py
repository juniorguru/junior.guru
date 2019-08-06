from pathlib import Path

import arrow
from jinja2 import Environment, Markup


BASE_URL = 'https://junior.guru'
PACKAGE_DIR = Path(__file__).parent
PROJECT_DIR = PACKAGE_DIR.parent
BUILD_DIR = PROJECT_DIR / 'build'


def render_template(url_path, template_path, data, filters=None):
    env = Environment()
    env.filters['email_link'] = email_link
    env.filters.update(filters or {})

    template = env.from_string(template_path.read_text())

    html_path = get_html_path(BUILD_DIR, url_path)
    html_path.parent.mkdir(parents=True, exist_ok=True)

    data['base_template'] = env.from_string((PACKAGE_DIR / 'base.html').read_text())
    data['list_note_template'] = env.from_string((PACKAGE_DIR / 'list_note.html').read_text())
    data['url'] = get_url(BASE_URL, url_path)
    data['url_path'] = url_path
    data['html_path'] = str(html_path.relative_to(BUILD_DIR))
    data['updated_at'] = arrow.utcnow()

    html_path.write_text(template.render(**data))


def get_url(base_url, url_path):
    return '/'.join(filter(None, [base_url.rstrip('/'), url_path.lstrip('/')]))


def get_html_path(build_dir, url_path):
    html_path = Path(build_dir) / url_path.lstrip('/')
    if not html_path.suffix:
        return html_path / 'index.html'
    return html_path


def email_link(email, text_template='{email}'):
    user, server = email.split('@')
    text = text_template.format(email=f'{user}&#64;<!---->{server}')
    return Markup(f'<a href="mailto:{user}&#64;{server}">{text}</a>')
