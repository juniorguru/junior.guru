import itertools
import math
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import click
from slugify import slugify

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.memberful import MemberfulAPI, MemberfulCSV, memberful_url
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.subscription import (
    SubscriptionCancellation,
    SubscriptionCancellationReason,
    SubscriptionInternalReferrer,
    SubscriptionMarketingSurvey,
    SubscriptionReferrer,
)


MEMBERS_GQL_PATH = Path(__file__).parent / "members.gql"


logger = loggers.from_path(__file__)


Row = dict[str, str]


@cli.sync_command()
@click.option(
    "--error-channel", "error_channel_id", default="business", type=parse_channel
)
@db.connection_context()
def main(error_channel_id: int):
    logger.info("Preparing")
    memberful = MemberfulAPI()

    tables = [
        SubscriptionReferrer,
        SubscriptionInternalReferrer,
        SubscriptionMarketingSurvey,
        SubscriptionCancellation,
    ]
    db.drop_tables(tables)
    db.create_tables(tables)

    try:
        logger.info("Fetching all members from Memberful API")
        members = list(
            logger.progress(memberful.get_nodes(MEMBERS_GQL_PATH.read_text()))
        )
        logger.info(f"Got {len(members)} members")
        emails = {member["email"]: int(member["id"]) for member in members}
        total_spend = {
            int(member["id"]): math.ceil(member["totalSpendCents"] / 100)
            for member in members
        }

        logger.info("Fetching members data from Memberful CSV")
        memberful = MemberfulCSV()
        seen_account_ids = set()
        for csv_row in memberful.download_csv(
            path="/admin/members/exports",
            form_params={
                "csv_export[filter]": "active",
                "csv_export[preset]": "all_time",
                "commit": "Export",
            },
        ):
            account_id = int(csv_row["Memberful ID"])
            if account_id in seen_account_ids:
                # This CSV sometimes contains multiple rows for the same account if the account
                # has different plans etc. We do not really care about those fields, so we treat
                # the rows as duplicates to simplify further code.
                continue
            seen_account_ids.add(account_id)

            referrer = csv_row["Referrer"] or None
            if referrer:
                account_details = dict(
                    account_id=account_id,
                    account_name=csv_row["Full Name"],
                    account_email=csv_row["Email"],
                    account_total_spend=total_spend[account_id],
                )
                created_on = date.fromisoformat(csv_row["Created at"])
                referrer_type = classify_referrer(referrer)
                if referrer_type.startswith("/"):
                    SubscriptionInternalReferrer.create(
                        created_on=created_on,
                        url=referrer,
                        path=referrer_type,
                        **account_details,
                    )
                else:
                    SubscriptionReferrer.create(
                        created_on=created_on,
                        url=referrer,
                        type=referrer_type,
                        **account_details,
                    )

            marketing_survey_answer = (
                csv_row["Jak ses dozvěděl(a) o junior.guru?"] or None
            )
            if marketing_survey_answer:
                marketing_survey_answer_type = classify_marketing_survey_answer(
                    marketing_survey_answer
                )
                SubscriptionMarketingSurvey.create(
                    account_id=account_id,
                    account_name=csv_row["Full Name"],
                    account_email=csv_row["Email"],
                    account_total_spend=total_spend[account_id],
                    created_on=date.fromisoformat(csv_row["Created at"]),
                    value=marketing_survey_answer,
                    type=marketing_survey_answer_type,
                )

        logger.info("Fetching cancellations data from Memberful CSV")
        csv_rows = itertools.chain(
            memberful.download_csv(
                path="/admin/csv_exports",
                url_params={
                    "filter": "all",
                    "type": "CancellationsCsvExport",
                },
            ),
            memberful.download_csv(
                path="/admin/csv_exports",
                url_params={
                    "filter": "all",
                    "type": "CancellationsCsvExport",
                    "scope": "completed",
                },
            ),
        )
        for csv_row in csv_rows:
            logger.debug(f"Processing cancellation:\n{csv_row!r}")
            if is_redacted_row(csv_row):
                logger.warning("Skipping redacted row")
                continue
            account_email = csv_row["Email"]
            if is_club_subscription(csv_row):
                logger.debug(f"Processing {account_email}")
                account_id = emails[account_email]
                logger.debug(f"Adding {memberful_url(account_id)} ({account_email})")
                SubscriptionCancellation.add(
                    account_id=account_id,
                    account_name=csv_row["Name"],
                    account_email=account_email,
                    account_total_spend=total_spend[account_id],
                    expires_on=get_date(csv_row),
                    reason=get_reason(csv_row),
                    feedback=get_feedback(csv_row),
                )
            else:
                logger.debug(f"Skipping {account_email}, not a club subscription")
    except Exception as e:
        logger.exception("Failed to fetch data from Memberful")
        discord_task.run(report_exception, error_channel_id, e)


@db.connection_context()
async def report_exception(client: ClubClient, channel_id: int, exception: Exception):
    logger.info("Reporting error to Discord")
    channel = await client.fetch_channel(channel_id)
    with mutating_discord(channel) as proxy:
        await proxy.send(
            f"Failed to fetch CSV data from Memberful:\n```\n{exception}\n```"
        )


def classify_referrer(url: str) -> str:
    parts = urlparse(url)
    if parts.netloc == "junior.guru":
        return parts.path.rstrip("/") or "/"
    if parts.netloc == "t.co":
        return "twitter"
    if parts.netloc == "honzajavorek.cz":
        return "honzajavorek"
    domain = parts.netloc.split(".")[-2]
    if domain in ("google", "facebook", "linkedin", "youtube"):
        return domain
    return "other"


def classify_marketing_survey_answer(text: str) -> str:
    text = text.strip()
    if re.search(r"\b(yablk\w+|rob\s*web)\b", text, re.I):
        return "yablko"
    if re.search(
        r"\b(pod[ck][aá]st\w*|spotify|rozbité prasátko|Street ?of ?Code)\b", text, re.I
    ):
        return "podcasts"
    if re.search(r"\brecenz\w+\b", text, re.I):
        return "courses_search"
    if re.search(r"\bpyladies\b", text, re.I):
        return "courses"
    if re.search(r"\bczechitas\b", text, re.I):
        return "courses"
    if re.search(
        r"\b(software\s+development\s+academy|sd\s*academy|sda\s+academy)\b", text, re.I
    ) or re.search(r"\bSDA\b", text):
        return "courses"
    if re.search(
        r"\b(kurz\w*|akademie|enget\w*|green\s*fox\w*|it\s*network\w*|nau[čc]\s+m[ěe]\s+it|webin[áa][řr]\w*)\b",
        text,
        re.I,
    ):
        return "courses"
    if re.search(r"\b(youtube|yt)\b", text, re.I):
        return "youtube"
    if re.search(r"\b(facebook\w*|fb|fcb)\b", text, re.I):
        return "facebook"
    if re.search(r"\blinkedin\w*\b", text, re.I) or re.search(r"\bLI\b", text):
        return "linkedin"
    if re.search(r"\b(goo?gl\w*|vyhled[aá]v\w+)\b", text, re.I):
        return "search"
    if re.search(
        r"\b(znám(ý|á)|komunit\w+|kamar[aá]d\w*|brat\w*|koleg\w*|br[aá]ch\w*|manžel\w*|partner\w*|p[řr][íi]a?tel\w*|přátelé|pratele|zn[áa]m[ée]\w*|doporu[čc]en\w+|Skládanka|Stan\w+ Prokop\w*|Tom\w* Hrn\w*)\b",
        text,
        re.I,
    ):
        return "friend"
    if re.search(r"^(tip\s+)?od\s+\w{3,}", text.strip(), re.I):
        return "friend"
    if re.search(
        r"\b(\w*hled[aá]\w+|h[ľl]ad[aá]\w+|search|na[šs]la|na[šs]i?el)\b", text, re.I
    ):
        return "search"
    if re.search(r"\binternet\w?\b", text, re.I):
        return "internet"
    if re.search(r"^(net\w?|web\w?|online)$", text, re.I):
        return "internet"
    if re.search(r"^\b\w{1,2}\s+(internet|web|net)\w*$", text, re.I):
        return "internet"
    return "other"


def get_reason(row: Row) -> SubscriptionCancellationReason:
    if row["Reason"]:
        return SubscriptionCancellationReason(slugify(row["Reason"], separator="_"))
    else:
        return SubscriptionCancellationReason.UNKNOWN


def get_feedback(row: Row) -> str:
    return row["Feedback"] or None


def is_club_subscription(row: Row) -> bool:
    return "členství v klubu" in row["Plan"].lower()


def get_date(row: Row) -> date:
    value = row.get("Date") or row.get("Expiration Date")
    if value == "N/A" or not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"Invalid date format: {value!r}")


def is_redacted_row(row: Row) -> bool:
    data = dict(row)
    data.pop("Plan")
    if re.search(r"^Member \d+$", data["Name"]):
        data.pop("Name")
    return set(data.values()) <= {None, "N/A", ""}
