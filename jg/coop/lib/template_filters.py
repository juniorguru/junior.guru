import math
import random
import re
from datetime import UTC
from numbers import Number
from operator import itemgetter
from typing import Generator, Iterable, Literal
from urllib.parse import unquote, urljoin
from zoneinfo import ZoneInfo

from markupsafe import Markup
from mkdocs.structure import StructureItem
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from slugify import slugify

from jg.coop.lib.md import md as md_
from jg.coop.lib.url_params import strip_utm_params


def email_link(email: str) -> Markup:
    user, server = email.split("@")
    return Markup(
        f'<a href="mailto:{user}&#64;{server}">{user}&#64;<!---->{server}</a>'
    )


def relative_url(url):
    return url.removeprefix("https://junior.guru")


def absolute_url(url):
    return urljoin("https://junior.guru", url)


def md(*args, **kwargs):
    return Markup(md_(*args, **kwargs))


def remove_p(html):
    return Markup(re.sub(r"</?p[^>]*>", "", html))


def local_time(dt):
    dt_utc = dt.replace(tzinfo=UTC)
    dt_prg = dt_utc.astimezone(ZoneInfo("Europe/Prague"))
    return dt_prg.strftime("%-H:%M")


def weekday(dt):
    return ["neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota"][
        int(dt.strftime("%w"))
    ]


def thousands(value):
    return re.sub(r"(\d)(\d{3})$", r"\1.\2", str(value))


def sample(items, n=2, sample_fn=None):
    items = list(items)
    if len(items) <= n:
        return items
    return (sample_fn or random.sample)(items, n)


def sample_jobs(jobs, n=2, sample_fn=None):
    jobs = list(jobs)
    if len(jobs) <= n:
        return jobs
    preferred_jobs = [job for job in jobs if job.is_submitted]
    if len(preferred_jobs) >= n:
        jobs = preferred_jobs
    return (sample_fn or random.sample)(jobs, n)


def icon(name, classes=None, alt=None):
    if classes:
        classes = set(filter(None, [cls.strip() for cls in classes.split(" ")]))
    else:
        classes = set()
    classes.add("bi")
    classes.add(f"bi-{name}")
    class_list = " ".join(sorted(classes))

    alt = f' role="img" aria-label="{alt}"' if alt else ""
    return Markup(f'<i class="{class_list}"{alt}></i>')


def docs_url(files, src_path):
    for file in files:
        if file.src_path == src_path:
            return file.url
    src_paths = ", ".join([f.src_path for f in files])
    raise ValueError(f"Could not find '{src_path}' in given MkDocs files: {src_paths}")


REVENUE_CATEGORIES = {
    "donations": "dobrovolné příspěvky",
    "jobs": "inzerce nabídek práce",
    "memberships": "členství v klubu",
    "sponsorships": "příspěvky sponzorů",
}


def revenue_categories(breakdown_mapping):
    return sorted(
        (
            (REVENUE_CATEGORIES[name], value)
            for name, value in breakdown_mapping.items()
        ),
        key=itemgetter(1),
        reverse=True,
    )


def money_breakdown_ptc(breakdown_mapping):
    items = list(breakdown_mapping.items())
    total = sum(item[1] for item in items)
    return {item[0]: math.ceil(item[1] * 100 / total) for item in items}


class TemplateError(Exception):
    pass


def assert_empty(collection: Iterable) -> Literal[""]:
    if len(collection):
        raise TemplateError(
            f"{type(collection).__name__} not empty: {', '.join(collection)}"
        )
    return ""


def screenshot_url(url: str) -> str:
    slug = slugify(nice_url(url))
    return f"static/screenshots/{slug}.webp"


def nice_url(url: str) -> str:
    return (
        unquote(strip_utm_params(url))
        .removeprefix("http://")
        .removeprefix("https://")
        .removeprefix("www.")
        .rstrip("/")
    )


def mapping(mapping: dict, keys: Iterable) -> list:
    return [mapping[key] for key in keys]


def mainnav(nav: Navigation) -> Generator[dict, None, None]:
    for item in list(nav)[:5]:
        first_child = _get_first_child(item)
        yield dict(title=item.title, url=first_child.url, is_active=item.active)


def subnav(nav: Navigation) -> Generator[dict, None, None]:
    mainnav_item = next(item for item in nav if item.active)
    for item in mainnav_item.children:
        first_child = _get_first_child(item)
        yield dict(title=item.title, url=first_child.url, is_active=item.active)


def _get_first_child(item: StructureItem) -> StructureItem:
    # for items without children, URL should result in the same
    # value as item.url, but for pages with a tree of descendants,
    # this ensures we use the first child's URL, regardless
    # of the depth where it resides
    children = [item]
    while children[0].children:
        children.insert(0, children[0].children[0])
    return children[0]


def toc(page: Page) -> Generator[dict, None, None]:
    # for pages without children, this should result in the same
    # value as page.parent, but for pages further down the tree,
    # this ensures we display only the top-level items, regardless
    # of the depth of the current page
    parents = [page]
    while parents[0].parent:
        parents.insert(0, parents[0].parent)
    parent = parents[0]

    # iterate over items
    for item in parent.children:
        if item.children:
            item_page = item.children[0]
        else:
            item_page = item
        yield dict(
            title=item_page.title,
            url=item_page.url,
            is_active=item.active,
            headings=[
                dict(title=heading.title, url=heading.url) for heading in item_page.toc
            ],
        )


def parent_page(page: Page) -> StructureItem | None:
    try:
        parent_page = page.parent.children[0]
        if parent_page == page:
            return page.parent.parent.children[0]
        return parent_page
    except AttributeError:
        return None


def sibling_page(page: Page, offset: int) -> StructureItem | None:
    try:
        index = page.parent.children.index(page)
        sibling_index = max(index + offset, 0)
        if index == sibling_index:
            return None
        return page.parent.children[sibling_index]
    except (AttributeError, IndexError):
        return None


def skip(items: Iterable, n: int) -> list:
    return list(items)[n:]


def shuffle(items: Iterable) -> list:
    items = list(items)
    random.shuffle(items)
    return items


def nplurals(
    value: Number,
    suffix_1: str,
    suffix_2: str,
    suffix_3: str,
) -> str:
    if value == 1:
        return suffix_1
    if 2 <= value <= 4:
        return suffix_2
    return suffix_3


def hours(seconds: int) -> str:
    minutes = seconds / 60
    if minutes <= 10:
        return f"{int(minutes)}min"
    if minutes < 70:
        rounded_minutes = math.ceil(minutes / 5) * 5
        if 50 <= rounded_minutes <= 70:
            return "1h"
        return f"{int(rounded_minutes)}min"
    hours = round((minutes / 60) * 2) / 2
    hours_str = str(int(hours)) if hours.is_integer() else str(hours).replace(".", ",")
    return f"{hours_str}h"
