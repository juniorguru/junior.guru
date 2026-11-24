import imaplib
from datetime import date

from jg.coop.lib import loggers


MONTHS = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


logger = loggers.from_path(__file__)


def fetch_emails(
    host: str, user: str, password: str, sender: str, since: date
) -> list[bytes]:
    """Returns raw emails from the given sender in INBOX, received on or after the given day"""
    logger.debug(f"Searching {host} INBOX for emails from {sender}")
    with imaplib.IMAP4_SSL(host) as imap:
        imap.login(user, password)
        imap.select("INBOX", readonly=True)
        _, data = imap.search(
            None, "FROM", f'"{sender}"', "SINCE", format_imap_date(since)
        )
        raw_emails = []
        for message_id in data[0].split():
            _, message_data = imap.fetch(message_id, "(BODY.PEEK[])")
            raw_emails.append(message_data[0][1])
    logger.debug(f"Found {len(raw_emails)} emails")
    return raw_emails


def format_imap_date(value: date) -> str:
    """Formats a date for IMAP search, independently of the system locale"""
    return f"{value.day}-{MONTHS[value.month - 1]}-{value.year}"
