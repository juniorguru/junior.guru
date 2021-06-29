from pathlib import Path

import jinja2

from mkdocs.utils.filters import tojson
from mkdocs.utils import normalize_url, get_relative_url

from juniorguru.lib import template_filters
from juniorguru.mkdocs import context as context_hooks


class MarkdownTemplateError(Exception):
    pass


def on_page_markdown(markdown, page, config, files):
    """Renders Markdown as if it was a Jinja2 template.

    Inspired by https://github.com/fralau/mkdocs_macros_plugin
    """
    macros_dir = Path(config['docs_dir']).parent / 'macros'
    loader = jinja2.FileSystemLoader(macros_dir)
    env = jinja2.Environment(loader=loader, auto_reload=False)

    def url(value):
        return normalize_url(value, page=page, base=get_relative_url('.', page.url))

    filters_names = config['template_filters']['shared'] + config['template_filters']['markdown']
    filters = {name: getattr(template_filters, name) for name in filters_names}
    filters['tojson'] = tojson
    filters['url'] = url
    env.filters.update(filters)

    context = {}
    context_hooks.on_shared_context(context, page, config)
    context_hooks.on_markdown_context(context, page, config)

    try:
        template = env.from_string(markdown)
        return template.render(**context)
    except Exception:
        raise MarkdownTemplateError(page)


def on_env(env, config, files):
    filters_names = config['template_filters']['shared'] + config['template_filters']['theme']
    filters = {name: getattr(template_filters, name) for name in filters_names}
    env.filters.update(filters)


def on_page_context(context, page, config, nav):
    context_hooks.on_shared_context(context, page, config)
    context_hooks.on_theme_context(context, page, config)
