"""Inserting non-breaking spaces into Czech text

Follows the rules of the Internet Language Reference Book by the Czech
Language Institute (https://prirucka.ujc.cas.cz/?id=880) as far as they
can be detected mechanically. Rules which require understanding of the
meaning (e.g. number followed by a name of counted things, initials of
first names) are not covered.
"""

import math
import re
from bisect import bisect_right


NBSP = "\u00a0"

JINJA = r"{{.*?}}|{%.*?%}|{\#.*?\#}"

# Parts of the markup which aren't Czech prose and must stay intact. Each regex
# is matched separately, because the parts can nest, e.g. Jinja inside an HTML
# attribute.
PROTECTED_RES = [
    re.compile(pattern, re.VERBOSE | re.DOTALL | re.MULTILINE)
    for pattern in [
        r"^[ \t]*(?P<fence>```|~~~).*?^[ \t]*(?P=fence)",  # fenced code block
        r"`[^`\n]+`",  # inline code
        r"{%-?\s*raw\s*-?%}.*?{%-?\s*endraw\s*-?%}",  # raw Jinja block
        JINJA,
        r"<!--.*?-->",  # HTML comment
        r"<(?P<element>pre|code|script|style)\b.*?</(?P=element)>",  # HTML code
        rf"</?[a-zA-Z](?:{JINJA}|[^<>])*>",  # HTML tag
        r"\]\([^)\n]*\)",  # Markdown link destination
        r"\{[:\#.][^}\n]*\}",  # Markdown attribute list
        r"https?://\S+|www\.\S+",  # URL
    ]
]

# Characters which can precede a number in prose, deliberately without newline
# so that numbered Markdown lists stay intact
NUMBER_START = r"(?<=[ („\"'\u00a0])"

UNITS = (
    "%",
    "‰",
    "°C",
    "°",
    "Kč",
    "€",
    "EUR",
    "USD",
    "CZK",
    "tis.",
    "mil.",
    "mld.",
    "hod.",
    "str.",
    "ms",
    "min",
    "h",
    "km",
    "cm",
    "mm",
    "m²",
    "m",
    "kg",
    "kB",
    "MB",
    "GB",
    "TB",
    "px",
    "ks",
)

TITLES = (
    "Bc.",
    "BcA.",
    "Mgr.",
    "MgA.",
    "Ing.",
    "Ing. arch.",
    "MUDr.",
    "MVDr.",
    "MDDr.",
    "JUDr.",
    "PhDr.",
    "RNDr.",
    "PharmDr.",
    "ThDr.",
    "PaedDr.",
    "doc.",
    "prof.",
)

# Each regex marks a span by the 'nbsp' group, where all spaces should be
# non-breaking
RULES_RES = [
    # one-letter prepositions and conjunctions, e.g. 'k mostu', 'i plné'
    re.compile(
        r"(?<![\w.,\-–/\\'’@#&=+*`~^$%])[ksvzouaiKSVZOUAI]"
        r"(?P<nbsp> )(?=[^\s\-–—|=+:;,.!?)\]}>])"
    ),
    # grouping of digits, e.g. '1 000 000', '+420 800 123 987'
    re.compile(
        rf"(?:{NUMBER_START}|(?<=\+))(?P<nbsp>\d{{1,3}}(?: \d{{3}})+)(?![\d,.]\d)"
    ),
    # number and its unit or sign, e.g. '50 %', '100 Kč', '16 h'
    re.compile(
        rf"{NUMBER_START}\d+(?:[,.]\d+)?(?P<nbsp> )"
        rf"(?:{'|'.join(map(re.escape, UNITS))})(?!\w)"
    ),
    # sign or abbreviation and a number, e.g. '§ 23', 'č. 9', 'obr. 1'
    re.compile(r"(?<![\w.])(?:§|č\.|s\.|str\.|obr\.|tab\.|kap\.)(?P<nbsp> )\d"),
    # ordinal number and a word or another number, e.g. '5. pluk', '21. 6.'
    re.compile(
        rf"{NUMBER_START}\d{{1,2}}\.(?P<nbsp> )(?:[a-zěščřžýáíéóůúťďň]|\d{{1,2}}\.)"
    ),
    # abbreviations bound to the following word, e.g. 'tzv. klikání'
    re.compile(r"(?<![\w.])(?:tj|tzv|tzn)\.(?P<nbsp> )\w"),
    # compound abbreviations, e.g. 's. r. o.', 'a. s.', 'v. v. i.'
    re.compile(
        r"(?<![\w.])(?P<nbsp>s\. r\. o\.|a\. s\.|v\. v\. i\.|(?:př\. )?n\. l\.)"
    ),
    # academic title before a name, e.g. 'Ing. Poliaková'
    re.compile(
        rf"(?<![\w.])(?:{'|'.join(map(re.escape, TITLES))})(?P<nbsp> )"
        r"[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]"
    ),
]


def add_nbsp(markup: str) -> str:
    """Replaces regular spaces with non-breaking ones where appropriate

    Never removes existing non-breaking spaces, only adds missing ones.
    Leaves code, Jinja, HTML tags, and URLs intact.
    """
    protected = get_protected_ranges(markup)
    positions = {
        position
        for rule_re in RULES_RES
        for match in rule_re.finditer(markup)
        for position in range(*match.span("nbsp"))
        if markup[position] == " " and not is_protected(position, protected)
    }
    if not positions:
        return markup
    chars = list(markup)
    for position in positions:
        chars[position] = NBSP
    return "".join(chars)


def get_protected_ranges(markup: str) -> list[tuple[int, int]]:
    """Returns sorted, non-overlapping spans of the protected parts"""
    spans = sorted(
        match.span()
        for protected_re in PROTECTED_RES
        for match in protected_re.finditer(markup)
    )
    merged = []
    for start, end in spans:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def is_protected(position: int, protected: list[tuple[int, int]]) -> bool:
    index = bisect_right(protected, (position, math.inf)) - 1
    return index >= 0 and position < protected[index][1]
