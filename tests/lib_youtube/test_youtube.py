import json
from pathlib import Path

import pytest

from jg.coop.lib.youtube import (
    parse_iso8601_duration,
    parse_youtube_id,
    parse_youtube_info,
)


@pytest.fixture
def raw_info():
    return json.loads((Path(__file__).parent / "info.json").read_text())


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://www.youtube.com/watch?v=0v5K4GvK4Gs", "0v5K4GvK4Gs"),
        ("https://youtu.be/0v5K4GvK4Gs", "0v5K4GvK4Gs"),
        (
            "https://www.youtube.com/watch?v=3-wsqhCK-wU&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_&index=5",
            "3-wsqhCK-wU",
        ),
    ],
)
def test_parse_youtube_id(url, expected):
    assert parse_youtube_id(url) == expected


def test_parse_youtube_id_raises():
    with pytest.raises(ValueError):
        parse_youtube_id("https://junior.guru")


def test_parse_youtube_info(raw_info: dict):
    info = parse_youtube_info(raw_info)

    assert info.model_dump() == {
        "id": "8_ZUwRKEJ7A",
        "url": "https://www.youtube.com/watch?v=8_ZUwRKEJ7A",
        "title": "Daniel Srb: Jak na CV při změně kariéry do IT (přednáška v rámci Týdne pro Digitální Česko)",
        "thumbnail_url": "https://i.ytimg.com/vi/8_ZUwRKEJ7A/maxresdefault.jpg",
        "description": "Jak napsat životopis při změně kariéry do IT? Záznam akce pro širokou veřejnost v rámci Týdne pro Digitální Česko. Všechny akce pod hlavičkou junior.guru najdeš na https://junior.guru/events/\n\n~~~ Popis ~~~\nDaniel Srb, který viděl spoustu CV, když nabíral vývojáře, pracoval také jako designér a již několik let provází klienty změnou kariéry do IT, ukáže, jak vytvořit efektivní životopis pro hledání první práce v IT. Představí i šablonu, která tě zdarma provede tvorbou kvalitního CV.\n\n~~~ Kapitoly ~~~\n0:00:00 Začátek streamu\n0:01:05 Úvod JG: Honza Javorek\n0:07:04 Začátek přednášky\n0:09:05 Proč CV věnovat pozornost\n0:12:26 Co o CV vlastně vím?\n0:16:08 Kvalitní CV\n0:17:59 Funkčnost CV\n0:22:36 Otázky\n0:31:09 Obsah CV\n0:33:37 Co do CV nepatří\n0:40:13 Otázky\n0:43:23 Co do CV patří\n0:45:37 Jméno a příjmení\n0:46:33 Název pozice\n0:47:11 Kontakty\n0:52:20 Souhrn\n1:06:04 Dovednosti\n1:13:50 Projekty\n1:31:24 Pracovní zkušenosti\n1:45:04 Vzdělání\n1:56:56 Soft skills\n2:01:10 Jazyky\n2:05:31 Zájmy\n2:08:13 Otázky\n2:15:35 Proces tvorby obsahu\n2:24:35 Nástroje na tvorbu CV\n2:31:22 Šablona CV pro switchery do IT\n2:35:12 Vzhled\n2:48:34 Dobře čitelný text\n2:53:12 Písmo\n3:05:42 Velikosti písma\n3:08:10 Vyznačování\n3:10:44 Logické celky a nadpisy\n3:12:45 Vynucené zalomení řádku\n3:13:51 Odkazy\n3:17:36 Odrážky\n3:19:02 Zarovnání textu\n3:21:25 Kdy porušit pravidla\n3:22:21 Délka CV (a jak zkrátit)\n3:31:35 Barvy\n3:33:51 Otázky\n3:35:57 Message from our sponsor\n3:37:14 Ukončení přednášky\n3:38:31 Ukončení přenosu: Honza Javorek\n3:43:28 Pozvánka na další stream JG",
        "duration_s": 13596,
        "view_count": 3364,
        "comment_count": 2,
        "like_count": 25,
    }


@pytest.mark.parametrize(
    "raw_key, key, expected",
    [
        ("viewCount", "view_count", 0),
        ("commentCount", "comment_count", 0),
        ("likeCount", "like_count", 0),
    ],
)
def test_parse_youtube_info_missing_stats(
    raw_info: dict, raw_key: str, key: str, expected: int
):
    del raw_info["statistics"][raw_key]
    info = parse_youtube_info(raw_info)

    assert info.model_dump()[key] == expected


@pytest.mark.parametrize(
    "duration, expected",
    [
        ("PT1H2M3S", 3723),
        ("PT1H2M", 3720),
        ("PT1H", 3600),
        ("PT2M3S", 123),
        ("PT2M", 120),
        ("PT3S", 3),
        ("PT0S", 0),
    ],
)
def test_parse_iso8601_duration(duration: str, expected: int):
    assert parse_iso8601_duration(duration) == expected
