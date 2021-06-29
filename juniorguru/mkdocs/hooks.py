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
    context = {}
    context_hooks.on_shared_context(context, page, config)
    context_hooks.on_markdown_context(context, page, config)

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


def on_page_context(context, page, config, nav):
    """Enhances the theme's template context."""
    context_hooks.on_shared_context(context, page, config)
    context_hooks.on_theme_context(context, page, config)
