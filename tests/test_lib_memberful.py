from datetime import UTC, datetime
from pathlib import Path

import pytest
from lxml import html

from jg.coop.lib.memberful import (
    checkout_url,
    is_one_time_code_url,
    is_student_pass_coupon,
    parse_created_coupons,
    parse_export_id,
    parse_one_time_code_email,
    parse_tier_name,
    read_trusted_browser,
    select_one_time_code,
    student_pass_coupon_code,
    student_pass_utm_params,
    write_trusted_browser,
)


FIXTURES_DIR = Path(__file__).parent / "lib_memberful"

SENT_AT = datetime(2026, 11, 24, 12, 39, 37, tzinfo=UTC)


@pytest.fixture
def one_time_code_email() -> bytes:
    return (FIXTURES_DIR / "one_time_code.eml").read_bytes()


def make_email(
    code: str,
    date: str = "Tue, 24 Nov 2026 12:39:37 +0000",
    sender: str = "Memberful <mail@memberful.com>",
) -> bytes:
    return (
        f"From: {sender}\r\n"
        f"Date: {date}\r\n"
        "Subject: Your one-time code for junior.guru\r\n"
        "Content-Type: text/plain; charset=UTF-8\r\n"
        "\r\n"
        "Enter this code to finish signing in. It works for 10 minutes.\r\n"
        "\r\n"
        f"{code}\r\n"
        "\r\n"
        "Memberful never asks for your password by email.\r\n"
    ).encode()


def test_parse_export_id_members():
    html_tree = html.fromstring(
        """
            <turbo-frame id="modal">
            <div class="sticky top-0 bg-white flex items-start justify-between md:min-w-[460px] gap-8 border-b pb-4 pt-6 mx-8 mb-4">
                <div class="flex flex-col gap-1">
                <h2 class="text-2xl font-semibold">Export members</h2>
                </div>
                <button type="button" class="w-9 h-9 flex items-center justify-center -mr-3 group" data-action="dialog#close">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" class="shrink-0 w-4 h-4 text-gray-600/70 group-hover:text-gray-700 fill-current group:text-gray-700"><title></title><path d="M10 8.586L2.929 1.515 1.515 2.929 8.586 10l-7.071 7.071 1.414 1.414L10 11.414l7.071 7.071 1.414-1.414L11.414 10l7.071-7.071-1.414-1.414L10 8.586z"></path></svg>
                <span class="sr-only">Close</span>
                </button>
            </div>
            <div class="mx-8 pb-3">
            <div data-controller="reload" data-reload-delay-value="1000" data-auto-refreshable-url-value="/admin/members/exports/68748">
                <div class="modal-message">
                    <p>
                    <img class="inline mr-2" src="https://assets.memberful.com/assets/admin/settings-spinner-4741fa457b5ab66d93eeda68b11ca57d97464b60401d406f31186481e5b55865.gif" />
                    Preparing your export. It will take just a minute...
                    </p>
                </div>
            </div>
            </div>
            </turbo-frame>
        """
    )

    assert parse_export_id(html_tree) == 68748


def test_parse_export_id_cancellations():
    html_tree = html.fromstring(
        """
            <turbo-frame id="modal">
            <div class="sticky top-0 bg-white flex items-start justify-between md:min-w-[460px] gap-8 border-b pb-4 pt-6 mx-8 mb-4">
                <div class="flex flex-col gap-1">
                <h2 class="text-2xl font-semibold">Export</h2>
                </div>
                <button type="button" class="w-9 h-9 flex items-center justify-center -mr-3 group" data-action="dialog#close">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" class="shrink-0 w-4 h-4 text-gray-600/70 group-hover:text-gray-700 fill-current group:text-gray-700"><title></title><path d="M10 8.586L2.929 1.515 1.515 2.929 8.586 10l-7.071 7.071 1.414 1.414L10 11.414l7.071 7.071 1.414-1.414L11.414 10l7.071-7.071-1.414-1.414L10 8.586z"></path></svg>
                <span class="sr-only">Close</span>
                </button>
            </div>
            <div class="mx-8 pb-3">
            <div class="mb-4" data-controller="reload" data-reload-delay-value="1000" data-auto-refreshable-url-value="/admin/csv_exports/68751">
                <div class="text-base text-gray-800">
                    <p>
                    Preparing your export. It will take just a minute...
                    </p>
                    <p class="mt-5 text-sm text-[#999]">
                    <img class="float-left mr-2.5" src="https://assets.memberful.com/assets/admin/settings-spinner-4741fa457b5ab66d93eeda68b11ca57d97464b60401d406f31186481e5b55865.gif" />
                    0 / 24
                    </p>
                </div>
            </div>
            </div>
            </turbo-frame>
        """
    )

    assert parse_export_id(html_tree) == 68751


@pytest.mark.parametrize(
    "name, expected",
    [
        ("Tarif „Budujeme brand“", "Budujeme brand"),
        ("Tarif „Voníme“", "Voníme"),
    ],
)
def test_parse_tier_name(name: str, expected: str):
    assert parse_tier_name(name) == expected


@pytest.mark.parametrize(
    "name",
    [
        "Roční členství v klubu",
        "Mentoring „CoreSkill“",
        "Klubové lekce angličtiny",
    ],
)
def test_parse_tier_name_raises(name: str):
    with pytest.raises(ValueError):
        parse_tier_name(name)


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://juniorguru.memberful.com/admin/auth/magic_link/edit", True),
        ("https://juniorguru.memberful.com/admin", False),
        ("https://juniorguru.memberful.com/admin/auth/sign_in", False),
    ],
)
def test_is_one_time_code_url(url: str, expected: bool):
    assert is_one_time_code_url(url) is expected


def test_parse_one_time_code_email(one_time_code_email: bytes):
    assert parse_one_time_code_email(one_time_code_email) == (SENT_AT, "JXIJJ3")


def test_parse_one_time_code_email_other_sender():
    raw_email = make_email("ABC123", sender="Someone <someone@example.com>")

    assert parse_one_time_code_email(raw_email) is None


def test_parse_one_time_code_email_no_code():
    raw_email = make_email("Thanks for signing in.")

    assert parse_one_time_code_email(raw_email) is None


def test_select_one_time_code_picks_newest():
    raw_emails = [
        make_email("OLD111", "Tue, 24 Nov 2026 12:40:00 +0000"),
        make_email("NEW222", "Tue, 24 Nov 2026 12:45:00 +0000"),
        make_email("MID333", "Tue, 24 Nov 2026 12:42:00 +0000"),
    ]

    assert select_one_time_code(raw_emails, SENT_AT) == "NEW222"


def test_select_one_time_code_ignores_older():
    raw_emails = [make_email("OLD111", "Tue, 24 Nov 2026 12:30:00 +0000")]

    assert select_one_time_code(raw_emails, SENT_AT) is None


def test_select_one_time_code_compares_timezones():
    raw_emails = [make_email("ABC123", "Tue, 24 Nov 2026 13:40:00 +0100")]

    assert select_one_time_code(raw_emails, SENT_AT) == "ABC123"


def test_select_one_time_code_empty():
    assert select_one_time_code([], SENT_AT) is None


def test_read_trusted_browser_missing(tmp_path: Path):
    assert read_trusted_browser(tmp_path / "trusted_browser") is None


def test_read_trusted_browser_empty(tmp_path: Path):
    path = tmp_path / "trusted_browser"
    path.write_text("\n")

    assert read_trusted_browser(path) is None


def test_write_and_read_trusted_browser(tmp_path: Path):
    path = tmp_path / "nested" / "trusted_browser"
    write_trusted_browser(path, "abc123")

    assert read_trusted_browser(path) == "abc123"


def test_checkout_url():
    assert checkout_url(123) == "https://juniorguru.memberful.com/checkout?plan=123"


def test_checkout_url_with_coupon_and_utm_params():
    url = checkout_url(123, coupon="KURZABC", utm_params={"utm_campaign": "x"})

    assert url == (
        "https://juniorguru.memberful.com/checkout"
        "?plan=123&coupon=KURZABC&utm_campaign=x"
    )


def test_student_pass_coupon_code():
    assert student_pass_coupon_code("czechitas") == "KURZCZECHITAS"


@pytest.mark.parametrize("slug", ["foo-bar", "foo_bar", "foo bar", "č"])
def test_student_pass_coupon_code_invalid(slug: str):
    with pytest.raises(ValueError):
        student_pass_coupon_code(slug)


@pytest.mark.parametrize(
    "code, expected",
    [
        ("KURZCZECHITAS", True),
        ("kurzczechitas", True),
        ("FINAID123", False),
        ("", False),
        (None, False),
    ],
)
def test_is_student_pass_coupon(code: str | None, expected: bool):
    assert is_student_pass_coupon(code) is expected


def test_parse_created_coupons():
    payload = {
        "createCoupons": {
            "coupons": [{"code": "KURZABC"}, {"code": "KURZXYZ"}],
            "errors": [],
        }
    }

    assert parse_created_coupons(payload) == ["KURZABC", "KURZXYZ"]


def test_parse_created_coupons_tolerates_taken_codes():
    payload = {
        "createCoupons": {
            "coupons": [{"code": "KURZXYZ"}],
            "errors": [
                {
                    "key": "KURZABC",
                    "messages": [{"attribute": "code", "message": "Code is taken."}],
                }
            ],
        }
    }

    assert parse_created_coupons(payload) == ["KURZXYZ"]


def test_parse_created_coupons_raises_on_other_errors():
    payload = {
        "createCoupons": {
            "coupons": [],
            "errors": [
                {
                    "key": "KURZ_ABC",
                    "messages": [{"attribute": "code", "message": "Code is invalid."}],
                }
            ],
        }
    }

    with pytest.raises(ValueError):
        parse_created_coupons(payload)


def test_student_pass_utm_params():
    assert student_pass_utm_params("czechitas") == {
        "utm_source": "student_pass",
        "utm_medium": "web",
        "utm_campaign": "course-czechitas",
    }
