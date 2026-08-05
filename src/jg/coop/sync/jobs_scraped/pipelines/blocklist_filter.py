import re

from jg.coop.sync.jobs_scraped import DropItem


BLOCKLIST = [
    ("title", re.compile(r"^(?!.*\bjunior).*\bsenior.*$", re.IGNORECASE)),
    ("title", re.compile(r"\b(plc|cnc|cad|cam)\s+program", re.IGNORECASE)),
    ("title", re.compile(r"\bprogramátor.+", re.IGNORECASE)),
    ("title", re.compile(r"\belektr", re.IGNORECASE)),
    ("title", re.compile(r"\břidič", re.IGNORECASE)),
    ("title", re.compile(r"\bkonstruktér", re.IGNORECASE)),
    ("title", re.compile(r"\bcomissioning", re.IGNORECASE)),
    ("title", re.compile(r"\boperátor\s+výroby", re.IGNORECASE)),
    ("title", re.compile(r"\bcae\s+inženýr", re.IGNORECASE)),
    ("title", re.compile(r"\bseřizovač", re.IGNORECASE)),
    ("title", re.compile(r"\bmana(ž|g)er", re.IGNORECASE)),
    ("title", re.compile(r"\bvedouc[íi]", re.IGNORECASE)),
    ("title", re.compile(r"\barchite(k|c)t", re.IGNORECASE)),
    ("title", re.compile(r"\bmarketing", re.IGNORECASE)),
    ("title", re.compile(r"\bdesigner|dizajn[é|e]r", re.IGNORECASE)),
    ("title", re.compile(r"\blead\b|\bleader|\blídr", re.IGNORECASE)),
    ("company_name", re.compile(r"Advantage Consulting", re.IGNORECASE)),
    ("company_name", re.compile(r"Hitachi Energy", re.IGNORECASE)),
    ("company_name", re.compile(r"SPORTISIMO", re.IGNORECASE)),
    ("company_name", re.compile(r"Jobs Contact Personal", re.IGNORECASE)),
    ("company_name", re.compile(r"INIZIO", re.IGNORECASE)),
    (
        "description_html",
        re.compile(r"\b(plc|cnc|cad|cam)\s+programátor", re.IGNORECASE),
    ),
]


async def process(item: dict) -> dict:
    for field, value_re in BLOCKLIST:
        value = item.get(field) or ""
        if value_re.search(value):
            raise DropItem(
                f"Blocklist rule applied: {field} value {value!r} matches {value_re.pattern!r}"
            )
    return item
