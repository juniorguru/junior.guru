import re
from enum import StrEnum, auto


class EmploymentTypes(StrEnum):
    CONTRACT = auto()
    FULLTIME = auto()
    INTERNSHIP = auto()
    PARTTIME = auto()
    VOLUNTEERING = auto()


STOP_WORDS = [
    re.compile(r"\bwork\b"),
    re.compile(r"\bpráce\s+na\b"),
    re.compile(r"\bpráce\b"),
    re.compile(r"\bprogram[sy]?\b"),
]

SEPARATORS_RE = re.compile(r"[\-\s]+")

EMPLOYMENT_TYPES_MAPPING = {
    "částečný_úvazek": EmploymentTypes.PARTTIME,
    "contract": EmploymentTypes.CONTRACT,
    "dobrovolnictví": EmploymentTypes.VOLUNTEERING,
    "external_collaboration": EmploymentTypes.CONTRACT,
    "full_time": EmploymentTypes.FULLTIME,
    "fulltime": EmploymentTypes.FULLTIME,
    "internship": EmploymentTypes.INTERNSHIP,
    "neplacená_stáž": EmploymentTypes.INTERNSHIP,
    "paid_internship": EmploymentTypes.INTERNSHIP,
    "part_time": EmploymentTypes.PARTTIME,
    "parttime": EmploymentTypes.PARTTIME,
    "placená_stáž": EmploymentTypes.INTERNSHIP,
    "plný_úvazek": EmploymentTypes.FULLTIME,
    "stáž": EmploymentTypes.INTERNSHIP,
    "trainee": EmploymentTypes.INTERNSHIP,
    "unpaid_internship": EmploymentTypes.INTERNSHIP,
    "volunteering": EmploymentTypes.VOLUNTEERING,
    "zkrácený_úvazek": EmploymentTypes.PARTTIME,
    "praxe_a_stáže": EmploymentTypes.INTERNSHIP,
    "other": None,
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
    mapping_key = SEPARATORS_RE.sub("_", value.strip())
    try:
        employment_type = EMPLOYMENT_TYPES_MAPPING[mapping_key]
    except KeyError:
        raise ValueError(f"Unknown employment type: {employment_type}")
    else:
        return str(employment_type).lower() if employment_type else None
