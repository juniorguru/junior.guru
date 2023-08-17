from pathlib import Path

import jinja2
from mkdocs.utils import get_relative_url
from mkdocs.utils.filters import url_filter

from juniorguru.lib import template_filters, mkdocs_jinja
from juniorguru.lib.jinja_cache import BytecodeCache
from juniorguru.web import api, context as context_hooks


TEMPLATE_FILTERS = [
    "docs_url",
    "email_link",
    "icon",
    "thousands",
    "sample",
    "remove_p",
    "money_breakdown_ptc",
    "revenue_categories",
    "sample_jobs",
    "assert_empty",
    "relative_url",
    "screenshot_url",
    "absolute_url",
    "mapping",
    "local_time",
    "menu",
    "toc",
    "parent_page",
    "sibling_page",
]


mkdocs_jinja.monkey_patch()


class MarkdownTemplateError(Exception):
    pass


def on_pre_build(config):
    macros_dir = Path(config["docs_dir"]).parent / "macros"
    config["theme"].dirs.append(macros_dir)

    config["shared_context"] = {}
    context_hooks.on_shared_context(config["shared_context"])
    config["docs_context"] = {}
    context_hooks.on_docs_context(config["docs_context"])
    config["theme_context"] = {}
    context_hooks.on_theme_context(config["theme_context"])


def on_page_markdown(markdown, page, config, files):
    """Renders Markdown as if it was a Jinja2 template.

    Inspired by https://github.com/fralau/mkdocs_macros_plugin
    """
    macros_dir = Path(config["docs_dir"]).parent / "macros"
    loader = jinja2.FileSystemLoader(macros_dir)
    cache = BytecodeCache(".web_cache/jinja2")
    env = jinja2.Environment(loader=loader, auto_reload=False, bytecode_cache=cache)

    filters = {name: getattr(template_filters, name) for name in TEMPLATE_FILTERS}
    filters["url"] = url_filter
    filters["md"] = mkdocs_jinja.create_md_filter(page, config, files)
    env.filters.update(filters)

    context = dict(
        page=page,
        config=config,
        pages=files,
        base_url=get_relative_url(".", page.url),
        **config["shared_context"],
        **config["docs_context"]
    )
    context_hooks.on_shared_page_context(context, page, config, files)
    context_hooks.on_docs_page_context(context, page, config, files)

    try:
        template = env.from_string(markdown)
        return template.render(**context)
    except Exception:
        raise MarkdownTemplateError(page)


def on_env(env, config, files):
    filters = {name: getattr(template_filters, name) for name in TEMPLATE_FILTERS}

    def md(markdown):
        raise NotImplementedError(
            "Using Markdown inside theme templates isn't supported"
        )

    filters["md"] = md
    env.filters.update(filters)


def on_page_context(context, page, config, nav):
    context.update(config["shared_context"])
    context.update(config["theme_context"])
    context_hooks.on_shared_page_context(context, page, config, context["pages"])
    context_hooks.on_theme_page_context(context, page, config, context["pages"])


def on_post_build(config):
    api_dir = Path(config["site_dir"]) / "api"
    api_dir.mkdir(parents=True, exist_ok=True)

    api.build_events_ics(api_dir, config)
    api.build_events_honza_ics(api_dir, config)
    api.build_podcast_xml(api_dir, config)
    api.build_czechitas_csv(api_dir, config)
