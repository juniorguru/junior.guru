import pytest

from jg.coop.lib.nbsp import add_nbsp


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Procházej i plné úvazky", "Procházej i\u00a0plné úvazky"),
        ("k mostu, s bratrem, v Plzni", "k\u00a0mostu, s\u00a0bratrem, v\u00a0Plzni"),
        ("u babičky a o páté", "u\u00a0babičky a\u00a0o\u00a0páté"),
        ("V Praze a Brně", "V\u00a0Praze a\u00a0Brně"),
        ("Kurz a „Python“", "Kurz a\u00a0„Python“"),
        ("Přečti si a [článek](a.md)", "Přečti si a\u00a0[článek](a.md)"),
        ("stojí 1 000 000 Kč", "stojí 1\u00a0000\u00a0000\u00a0Kč"),
        ("volej +420 800 123 987", "volej +420\u00a0800\u00a0123\u00a0987"),
        ("sleva 50 %", "sleva 50\u00a0%"),
        ("teplota 19 °C", "teplota 19\u00a0°C"),
        ("trvá 16 h nebo 30 min", "trvá 16\u00a0h nebo 30\u00a0min"),
        ("viz § 23 a obr. 1", "viz §\u00a023 a\u00a0obr.\u00a01"),
        ("dne 21. 6. 2024", "dne 21.\u00a06. 2024"),
        ("narozen 16. ledna 1972", "narozen 16.\u00a0ledna 1972"),
        ("tzv. klikání", "tzv.\u00a0klikání"),
        ("firma s. r. o. a a. s.", "firma s.\u00a0r.\u00a0o. a\u00a0a.\u00a0s."),
        ("Ing. Poliaková", "Ing.\u00a0Poliaková"),
    ],
)
def test_add_nbsp(text: str, expected: str):
    assert add_nbsp(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "Procházej i\u00a0plné úvazky",
        "slovo\u00a0a slovo",
        "Python\u00a03",
    ],
)
def test_add_nbsp_keeps_existing_nbsp(text: str):
    assert add_nbsp(text).count("\u00a0") >= text.count("\u00a0")


def test_add_nbsp_is_idempotent():
    text = "k mostu a 1 000 Kč"

    assert add_nbsp(add_nbsp(text)) == add_nbsp(text)


@pytest.mark.parametrize(
    "text",
    [
        "Napiš `a = 1 if x else 2`",
        "```python\nif a and b:\n    print(a or b)\n```",
        "  ~~~\n  x = a if b else c\n  ~~~",
        '{{ "a b"|icon }}',
        "{% call note('a b') %}",
        "{# a b #}",
        '<a href="/" class="a b">',
        "<pre>a b</pre>",
        "<script>if (a && b) { x = a ? 1 : 2 }</script>",
        "<!-- a b -->",
        "[odkaz](https://example.com/a b)",
        "{: .a b }",
        "https://example.com/?q=a b",
        "1. krok\n2. krok",
        "e-mail a- b",
        "x/a b",
        "| a | b |",
        "a - b",
        "Python 3 je super",
        "roce 2020 jsem",
        "A. Potom",
    ],
)
def test_add_nbsp_leaves_intact(text: str):
    assert add_nbsp(text) == text


def test_add_nbsp_leaves_intact_jinja_inside_html_attribute():
    text = '<td class="goal{% if progress >= 100 %} goal-reached{% endif %}">'

    assert add_nbsp(text) == text
