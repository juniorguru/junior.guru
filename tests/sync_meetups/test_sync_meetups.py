import itertools
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from jg.core.lib.discord_club import ClubMemberID
from jg.core.sync.meetups import (
    generate_scheduled_event,
    generate_starting_message_content,
    generate_thread_message_content,
    is_meetup_scheduled_event,
    isnt_skipped,
    parse_icalendar,
    parse_meetup_com_location,
    parse_meetup_url,
    thread_name,
)


StubScheduledEvent = namedtuple(
    "ScheduledEvent", ["name", "creator_id"], defaults=[123]
)


@pytest.fixture
def icalendar_content() -> str:
    return (Path(__file__).parent / "pyvo.ics").read_text()


@pytest.fixture
def icalendar_tentative_content() -> str:
    return (Path(__file__).parent / "pyvo_tentative.ics").read_text()


@pytest.fixture
def event() -> dict[str, Any]:
    return dict(
        location=("Rohanské nábř. 19, 186 00 Karlín", "Praha"),
        location_raw="Applifting, Rohanské nábř. 19, Praha",
        name="Mini sraz juniorů na akci pythonistů",
        name_raw="ReactGirls & Applifting meetup",
        starts_at=datetime(2021, 6, 24, 18, 30),
        url="https://www.meetup.com/reactgirls/events/292684010/",
        emoji="⚛️",
    )


def test_parse_icalendar(icalendar_content: str):
    events = parse_icalendar(icalendar_content)
    keys = set(itertools.chain.from_iterable(event.keys() for event in events))

    assert keys == {"name_raw", "starts_at", "location_raw", "url"}


def test_parse_icalendar_provides_timezone_aware_datetime(icalendar_content: str):
    events = parse_icalendar(icalendar_content)
    have_timezone = [event["starts_at"].tzinfo for event in events]

    assert all(have_timezone)


def test_parse_icalendar_skips_tentative(icalendar_tentative_content: str):
    events = parse_icalendar(icalendar_tentative_content)

    assert [event["url"] for event in events] == ["https://pyvo.cz/brno-pyvo/2011-04/"]


def test_parse_meetup_com_location():
    venue = {
        "name": "Pipedrive",
        "address": "Pernerova 697/35, Karlín",
        "city": "Praha-Praha 8",
        "state": None,
        "country": "cz",
    }

    assert (
        parse_meetup_com_location(venue)
        == "Pipedrive, Pernerova 697/35, Karlín, Praha-Praha 8, CZ"
    )


def test_parse_meetup_com_location_online_event():
    venue = {
        "address": None,
        "city": None,
        "country": None,
        "name": "Online event",
        "state": None,
    }

    with pytest.raises(ValueError):
        assert parse_meetup_com_location(venue)


@pytest.mark.parametrize(
    "event, skipped, expected",
    [
        ({"name_raw": "Pyvo Meetup"}, None, True),
        ({"name_raw": "Pyvo Meetup"}, [], True),
        ({"name_raw": "Pyvo Meetup"}, ["konference"], True),
        ({"name_raw": "konference"}, ["konference"], False),
        ({"name_raw": "Konference"}, ["konference"], False),
        (
            {
                "name_raw": "VYPRODÁNO FrontKon 2023 - konference komunity Frontendisti.cz"
            },
            ["konference"],
            False,
        ),
        (
            {"name_raw": "Celodenní Workshop: Aplikace na správu seznamu studentů"},
            ["workshop"],
            False,
        ),
    ],
)
def test_isnt_skipped(event: dict[str, Any], skipped: list[str], expected: bool):
    assert isnt_skipped(event, skipped) is expected


@pytest.mark.parametrize(
    "scheduled_event, expected",
    [
        (StubScheduledEvent("Pyvo Meetup"), False),
        (StubScheduledEvent("Pyvo Meetup", creator_id=ClubMemberID.BOT), False),
        (StubScheduledEvent("Praha: Mini sraz juniorů na akci pythonistů"), False),
        (
            StubScheduledEvent(
                "Praha: Mini sraz juniorů na akci pythonistů",
                creator_id=ClubMemberID.BOT,
            ),
            True,
        ),
    ],
)
def test_is_meetup_scheduled_event(scheduled_event, expected):
    assert is_meetup_scheduled_event(scheduled_event) is expected


def test_parse_meetup_url():
    text = (
        "**Akce:** ReactGirls & Applifting meetup\n"
        "**Více info:** https://www.meetup.com/reactgirls/events/292684010/\n\n"
        "Chceš se poznat s lidmi z klubu i naživo? Běžně se potkáváme na srazech vybraných komunit. Utvořte skupinku, ničeho se nebojte, a vyrazte!"
    )
    assert (
        parse_meetup_url(text) == "https://www.meetup.com/reactgirls/events/292684010/"
    )


def test_generate_scheduled_event(event: dict):
    params = generate_scheduled_event(event)

    assert sorted(params.keys()) == [
        "description",
        "end_time",
        "location",
        "name",
        "start_time",
    ]
    assert params["name"] == "Praha: Mini sraz juniorů na akci pythonistů"
    assert "ReactGirls & Applifting meetup" in params["description"]
    assert (
        "https://www.meetup.com/reactgirls/events/292684010/" in params["description"]
    )
    assert params["start_time"] == datetime(2021, 6, 24, 18, 30)
    assert params["end_time"] == datetime(2021, 6, 24, 21, 30)
    assert params["location"] == "Applifting, Rohanské nábř. 19, Praha"


def test_generate_starting_message_content(event: dict):
    text = generate_starting_message_content(event)

    assert "ReactGirls & Applifting meetup" in text
    assert "⚛️" in text
    assert "https://www.meetup.com/reactgirls/events/292684010/" in text


def test_thread_name(event: dict):
    assert thread_name(event) == "Praha, 24.6. – ReactGirls & Applifting meetup"


def test_thread_name_too_long(event: dict):
    event["name_raw"] = (
        "Pražské Pyvo #149 Engineering Of Structured, Semi-Structured And Unstructured Data & Language Models and the Non-English Languages"
    )
    name = thread_name(event, limit=40)

    assert len(name) == 40
    assert name == "Praha, 24.6. – Pražské Pyvo #149 Engine…"


def test_generate_thread_message():
    text = generate_thread_message_content(
        "https://discord.com/events/769966886598737931/1132525354439946310",
        ["@jarda", "@tajtrlik", "@alena"],
    )

    assert "https://discord.com/events/769966886598737931/1132525354439946310" in text
    assert "potkáš" in text
    assert "@alena @jarda @tajtrlik" in text


def test_generate_thread_message_without_mentions():
    text = generate_thread_message_content(
        "https://discord.com/events/769966886598737931/1132525354439946310"
    )

    assert "https://discord.com/events/769966886598737931/1132525354439946310" in text
    assert "potkáš" not in text
    assert "@" not in text
