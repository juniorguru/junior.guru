from pathlib import Path

from mkdocs.config.base import Config
from mkdocs.utils import get_relative_url
from mkdocs.utils.templates import TemplateContext

from jg.coop.lib import mkdocs_jinja
from jg.coop.web import api, context as context_hooks


mkdocs_jinja.monkey_patch()


def on_pre_build(config):
    config["theme"].dirs.append(mkdocs_jinja.get_macros_dir(config))
    config["shared_context"] = {}
    context_hooks.on_shared_context(config["shared_context"])
    config["docs_context"] = {}
    context_hooks.on_docs_context(config["docs_context"])
    config["theme_context"] = {}
    context_hooks.on_theme_context(config["theme_context"])


def on_page_markdown(markdown, page, config, files) -> str:
    """Renders Markdown as if it was a Jinja template.

    Inspired by https://github.com/fralau/mkdocs_macros_plugin
    """
    env = mkdocs_jinja.get_env(page, config, files)
    context = dict(
        page=page,
        config=config,
        pages=files,
        base_url=get_relative_url(".", page.url),
        **config["shared_context"],
        **config["docs_context"],
    )
    context_hooks.on_shared_page_context(context, page, config, files)
    context_hooks.on_docs_page_context(context, page, config, files)
    template = env.from_string(markdown)
    return template.render(**context)


def on_env(env, config, files):
    filters = mkdocs_jinja.get_filters()

    def md(markdown):
        raise NotImplementedError(
            "Using Markdown inside theme templates isn't supported"
        )

    filters["md"] = md
    env.filters.update(filters)


def on_template_context(
    context: TemplateContext, template_name: str, config: Config
) -> None:
    if template_name == "404.html":
        context.update(config["shared_context"])
        context.update(config["theme_context"])


def on_page_context(context, page, config, nav):
    context.update(config["shared_context"])
    context.update(config["theme_context"])
    context_hooks.on_shared_page_context(context, page, config, context["pages"])
    context_hooks.on_theme_page_context(context, page, config, context["pages"])


def on_post_build(config):
    api_dir = Path(config["site_dir"]) / "api"
    api_dir.mkdir(parents=True, exist_ok=True)

    api.build_course_providers_api(api_dir, config)
    api.build_interests_api(api_dir, config)
    api.build_events_ics(api_dir, config)
    api.build_events_honza_ics(api_dir, config)
    api.build_podcast_xml(api_dir, config)
    api.build_czechitas_csv(api_dir, config)
