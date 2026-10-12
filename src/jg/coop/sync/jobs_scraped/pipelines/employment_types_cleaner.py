import re
from enum import StrEnum, auto

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


class EmploymentTypes(StrEnum):
    CONTRACT = auto()
    FULLTIME = auto()
    INTERNSHIP = auto()
    PARTTIME = auto()
    VOLUNTEERING = auto()
    TEMPORARY = auto()


STOP_WORDS = [
    re.compile(r"\bwork\b"),
    re.compile(r"\bprác[ea]\s+na\b"),
    re.compile(r"\bprác[ea]\b"),
    re.compile(r"\bprogram[sy]?\b"),
]

SEPARATORS_RE = re.compile(r"[\-\s]+")

EMPLOYMENT_TYPES_MAPPING = {
    "brigáda": EmploymentTypes.TEMPORARY,
    "částečný úvazek": EmploymentTypes.PARTTIME,
    "contract": EmploymentTypes.CONTRACT,
    "dobrovolnictví": EmploymentTypes.VOLUNTEERING,
    "dohoda": EmploymentTypes.TEMPORARY,
    "external collaboration": EmploymentTypes.CONTRACT,
    "full time": EmploymentTypes.FULLTIME,
    "fulltime": EmploymentTypes.FULLTIME,
    "internship": EmploymentTypes.INTERNSHIP,
    "jiný typ": None,
    "na dohodu": EmploymentTypes.TEMPORARY,
    "na dohodu (brigády)": EmploymentTypes.TEMPORARY,
    "neplacená stáž": EmploymentTypes.INTERNSHIP,
    "other": None,
    "paid internship": EmploymentTypes.INTERNSHIP,
    "part time": EmploymentTypes.PARTTIME,
    "parttime": EmploymentTypes.PARTTIME,
    "placená stáž": EmploymentTypes.INTERNSHIP,
    "plný úvazek": EmploymentTypes.FULLTIME,
    "plný úväzok": EmploymentTypes.FULLTIME,
    "praxe a stáže": EmploymentTypes.INTERNSHIP,
    "skrátený úväzok": EmploymentTypes.PARTTIME,
    "stáž": EmploymentTypes.INTERNSHIP,
    "temporary": EmploymentTypes.TEMPORARY,
    "trainee": EmploymentTypes.INTERNSHIP,
    "unpaid internship": EmploymentTypes.INTERNSHIP,
    "volunteer": EmploymentTypes.VOLUNTEERING,
    "volunteering": EmploymentTypes.VOLUNTEERING,
    "zkrácený úvazek": EmploymentTypes.PARTTIME,
    "zkrátený úväzok": EmploymentTypes.PARTTIME,
    "živnost": EmploymentTypes.CONTRACT,
    "živnosť": EmploymentTypes.CONTRACT,
}


async def process(item: dict) -> dict:
    if item.get("employment_types"):
        item["employment_types"] = clean_employment_types(item["employment_types"])
    return item


def clean_employment_types(employment_types: list[str]) -> list[str]:
    return sorted(set(filter(None, map(clean_employment_type, employment_types))))


def clean_employment_type(employment_type: str) -> str | None:
    value = employment_type.lower()
    for stop_word_re in STOP_WORDS:
        value = stop_word_re.sub("", value)
    mapping_key = SEPARATORS_RE.sub(" ", value.strip())
    try:
        employment_type = EMPLOYMENT_TYPES_MAPPING[mapping_key]
    except KeyError:
        logger.warning(f"Unknown employment type: {employment_type!r}")
        return None
    else:
        return str(employment_type).lower() if employment_type else None
