import re
from enum import StrEnum


def regex(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.I)


class Names(StrEnum):
    GOVCZ = "govcz"
    JOBSCZ = "jobscz"
    JUNIORGURU = "juniorguru"
    LINKEDIN = "linkedin"
    STARTUPJOBS = "startupjobs"


REGEXES = [
    (Names.JUNIORGURU, regex(r"\bjunior\.guru/jobs/(?P<id>[0-9a-fA-F]+)")),
    (
        Names.GOVCZ,
        regex(
            r"\bportal\.isoss\.gov\.cz/irj/portal/anonymous/eosmlistpublic#/detail/(?P<id>\d+)"
        ),
    ),
    (Names.STARTUPJOBS, regex(r"\bstartupjobs\.cz/nabidka/(?P<id>\d+/[^/]+)")),
    (Names.JOBSCZ, regex(r"\bwww\.jobs\.cz/rpd/(?P<id>\d+)")),
    (Names.JOBSCZ, regex(r"\bwww\.jobs\.cz/fp/[^/]+/(?P<id>\d+)")),
    (Names.JOBSCZ, regex(r"\.jobs\.cz/detail-pozice.*[\&\?]id=(?P<id>\d+)")),
    (Names.LINKEDIN, regex(r"\blinkedin\.com/jobs/view/([\w+\-%]+\-)?(?P<id>\d+)")),
]

TEMPLATES = {
    Names.JUNIORGURU: "https://junior.guru/jobs/{id}/",
    Names.GOVCZ: "https://portal.isoss.gov.cz/irj/portal/anonymous/eosmlistpublic#/detail/{id}",
    Names.STARTUPJOBS: "https://www.startupjobs.cz/nabidka/{id}",
    Names.JOBSCZ: "https://www.jobs.cz/rpd/{id}/",
    Names.LINKEDIN: "https://www.linkedin.com/jobs/view/{id}/",
}

ORDERING = list(TEMPLATES.keys())


def id_to_url(canonical_id: str) -> str:
    name, id_ = canonical_id.split("#", 1)
    try:
        return TEMPLATES[Names(name)].format(id=id_)
    except KeyError:
        raise NotImplementedError(f"No URL template for {name!r}")


def url_to_id(url) -> str | None:
    for name, id_regex in REGEXES:
        match = id_regex.search(url)
        if match:
            return f"{name}#{match.group('id')}"
    return None


def get_order(canonical_id: str) -> int:
    board_name = canonical_id.split("#", 1)[0]
    return ORDERING.index(board_name)


def urls_to_ids(urls: list[str]) -> list[str]:
    ids = filter(None, map(url_to_id, urls))
    return sorted(set(ids), key=get_order)
