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

    filters_names = config['template_filters']['shared'] + config['template_filters']['markdown']
    filters = {name: getattr(template_filters, name) for name in filters_names}
    filters['tojson'] = tojson
    filters['url'] = create_url_filter(page)
    filters['md'] = create_md_filter(page, config, files)
    env.filters.update(filters)

    context = {}
    context_hooks.on_shared_context(context, page, config, files)
    context_hooks.on_markdown_context(context, page, config, files)

    try:
        template = env.from_string(markdown)
        return template.render(**context)
    except Exception:
        raise MarkdownTemplateError(page)


def on_pre_build(config):
    macros_dir = Path(config['docs_dir']).parent / 'macros'
    config['theme'].dirs.append(macros_dir)


def on_env(env, config, files):
    filters_names = config['template_filters']['shared'] + config['template_filters']['theme']
    filters = {name: getattr(template_filters, name) for name in filters_names}
    env.filters.update(filters)


def on_page_context(context, page, config, nav):
    context_hooks.on_shared_context(context, page, config, context['pages'])
    context_hooks.on_theme_context(context, page, config, context['pages'])


def create_url_filter(page):
    def url(value):
        # Like the built-in MkDocs's own Jinja2 url filter, but this one is to be used with
        # Jinja2 pre-processing the Markdown files. From user's perspective, there should be
        # no percieved difference between the built-in filter when working on the theme, and
        # this one when writing the documents. It should look and feel the same.
        return normalize_url(value, page=page, base=get_relative_url('.', page.url))
    return url


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
