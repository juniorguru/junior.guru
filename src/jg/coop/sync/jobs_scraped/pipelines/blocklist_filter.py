import re

from jg.coop.sync.jobs_scraped import DropItem


BLOCKLIST = [
    ("title", re.compile(r"^(?!.*\bjunior).*\bsenior.*$", re.I)),
    ("title", re.compile(r"\b(plc|cnc|cad|cam)\s+program", re.I)),
    ("title", re.compile(r"\bprogramátor.+", re.I)),
    ("title", re.compile(r"\belektr", re.I)),
    ("title", re.compile(r"\břidič", re.I)),
    ("title", re.compile(r"\bkonstruktér", re.I)),
    ("title", re.compile(r"\bcomissioning", re.I)),
    ("title", re.compile(r"\boperátor\s+výroby", re.I)),
    ("title", re.compile(r"\bcae\s+inženýr", re.I)),
    ("title", re.compile(r"\bseřizovač", re.I)),
    ("title", re.compile(r"\bmana(ž|g)er", re.I)),
    ("title", re.compile(r"\bvedouc[íi]", re.I)),
    ("title", re.compile(r"\barchite(k|c)t", re.I)),
    ("title", re.compile(r"\bmarketing", re.I)),
    ("title", re.compile(r"\bdesigner|dizajn[é|e]r", re.I)),
    ("title", re.compile(r"\blead\b|\bleader|\blídr", re.I)),
    ("company_name", re.compile(r"Advantage Consulting", re.I)),
    ("company_name", re.compile(r"Hitachi Energy", re.I)),
    ("company_name", re.compile(r"SPORTISIMO", re.I)),
    ("company_name", re.compile(r"Jobs Contact Personal", re.I)),
    ("company_name", re.compile(r"INIZIO", re.I)),
    ("description_html", re.compile(r"\b(plc|cnc|cad|cam)\s+programátor", re.I)),
]


async def process(item: dict) -> dict:
    for field, value_re in BLOCKLIST:
        value = item.get(field) or ""
        if value_re.search(value):
            raise DropItem(
                f"Blocklist rule applied: {field} value {value!r} matches {value_re.pattern!r}"
            )
    return item
