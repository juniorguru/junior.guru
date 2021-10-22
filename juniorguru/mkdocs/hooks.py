from pathlib import Path
import csv

import jinja2

from mkdocs.utils.filters import tojson, url_filter
from mkdocs.utils import get_relative_url

from juniorguru.lib import template_filters
from juniorguru.mkdocs import context as context_hooks
from juniorguru.models import Employment, with_db


TEMPLATE_FILTERS = [
    'docs_url',
    'email_link',
    'icon',
    'thousands',
    'sample',
    'metric',
    'remove_p',
    'metrics_inc_breakdown',
    'ago',
    'sample_jobs',
]


class MarkdownTemplateError(Exception):
    pass


def on_page_markdown(markdown, page, config, files):
    """Renders Markdown as if it was a Jinja2 template.

    Inspired by https://github.com/fralau/mkdocs_macros_plugin
    """
    macros_dir = Path(config['docs_dir']).parent / 'macros'
    loader = jinja2.FileSystemLoader(macros_dir)
    env = jinja2.Environment(loader=loader, auto_reload=False)

    filters = {name: getattr(template_filters, name) for name in TEMPLATE_FILTERS}
    filters['tojson'] = tojson
    filters['url'] = url_filter
    filters['md'] = create_md_filter(page, config, files)
    env.filters.update(filters)

    context = dict(page=page,
                   config=config,
                   pages=files,
                   base_url=get_relative_url('.', page.url))
    context_hooks.on_shared_context(context, page, config, files)
    context_hooks.on_docs_context(context, page, config, files)

    try:
        template = env.from_string(markdown)
        return template.render(**context)
    except Exception:
        raise MarkdownTemplateError(page)


def on_pre_build(config):
    macros_dir = Path(config['docs_dir']).parent / 'macros'
    config['theme'].dirs.append(macros_dir)


def on_env(env, config, files):
    filters = {name: getattr(template_filters, name) for name in TEMPLATE_FILTERS}
    def md(markdown):
        raise NotImplementedError("Using Markdown inside theme templates isn't supported")
    filters['md'] = md
    env.filters.update(filters)


def on_page_context(context, page, config, nav):
    context_hooks.on_shared_context(context, page, config, context['pages'])
    context_hooks.on_theme_context(context, page, config, context['pages'])


@with_db
def on_post_build(config):
    api_dir = Path(config['site_dir']) / 'api'
    api_dir.mkdir(parents=True, exist_ok=True)

    api_file = (api_dir / 'jobs.csv')
    rows = [employment.to_api() for employment in Employment.api_listing()]

    with api_file.open('w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def create_md_filter(page, config, files):
    def md(markdown):
        # Sorcery ahead! So this is a jinja2 filter, which takes a Markdown string, e.g. from
        # database, and turns it into HTML markup. One could just 'from markdown import markdown',
        # then call 'markdown(...)' and be done with it, but that wouldn't parse the input in the
        # context of MkDocs Markdown settings. Extensions wouldn't be set the same way. Relative
        # links wouldn't work. For that reason, we want to use the MkDocs' own Markdown rendering.
        #
        # Unfortunately, the Page.render() method isn't really meant to be used anywhere else:
        # https://github.com/mkdocs/mkdocs/blob/fd0e9dedd27e4cb628ab98ff2723165110b38ed2/mkdocs/structure/pages.py#L161
        #
        # The following sorcery works around that bit. It creates an artificial _Page object similar
        # to the real MkDocs' own Page object, but only with the properties used by the Page.render()
        # method. It sets all the configuration, passes the input as the 'markdown' property, and
        # steals the Page.render() method to behave like if it always belonged to the _Page object.
        # Then it calls this new _Page.render() method and returns the 'content' property, to which
        # the method sets the result of the rendering.
        #
        # This works, but is very prone to get broken if MkDocs changes something in their code.
        # In such case one needs to read the new MkDocs code and fix the solution accordingly.
        class _Page():
            def __init__(self):
                self.file = page.file
                self.markdown = markdown
                self.render = page.__class__.render.__get__(self)
        _page = _Page()
        _page.render(config, files)
        return _page.content
    return md
