import itertools
import math
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import click
from slugify import slugify

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.memberful import MemberfulAPI, MemberfulCSV
from juniorguru.models.base import db
from juniorguru.models.subscription import (
    SubscriptionCancellation,
    SubscriptionInternalReferrer,
    SubscriptionMarketingSurvey,
    SubscriptionReferrer,
)


MEMBERS_GQL_PATH = Path(__file__).parent / 'members.gql'


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option('--clear-cache/--keep-cache', default=False)
@click.pass_context
@db.connection_context()
def main(context, clear_cache):
    logger.info('Preparing')
    memberful = MemberfulAPI(cache_dir=context.obj['cache_dir'],
                             clear_cache=clear_cache)

    tables = [SubscriptionReferrer,
              SubscriptionInternalReferrer,
              SubscriptionMarketingSurvey,
              SubscriptionCancellation]
    db.drop_tables(tables)
    db.create_tables(tables)

    logger.info('Fetching all members from Memberful API')
    members = list(logger.progress(memberful.get_nodes(MEMBERS_GQL_PATH.read_text())))
    logger.info(f'Got {len(members)} members')
    emails = {member['email']: int(member['id']) for member in members}
    total_spend = {int(member['id']): math.ceil(member['totalSpendCents'] / 100) for member in members}

    logger.info("Fetching members data from Memberful CSV")
    memberful = MemberfulCSV(cache_dir=context.obj['cache_dir'], clear_cache=clear_cache)
    seen_account_ids = set()
    for csv_row in memberful.download_csv(dict(type='MembersCsvExport', filter='all')):
        account_id = int(csv_row['Memberful ID'])
        if account_id in seen_account_ids:
            # This CSV sometimes contains multiple rows for the same account if the account
            # has different plans etc. We do not really care about those fields, so we treat
            # the rows as duplicates to simplify further code.
            continue
        seen_account_ids.add(account_id)

        referrer = csv_row['Referrer'] or None
        if referrer:
            account_details = dict(account_id=account_id,
                                   account_name=csv_row['Full Name'],
                                   account_email=csv_row['Email'],
                                   account_total_spend=total_spend[account_id])
            created_on = date.fromisoformat(csv_row['Created at'])
            referrer_type = classify_referrer(referrer)
            if referrer_type.startswith('/'):
                SubscriptionInternalReferrer.create(created_on=created_on,
                                                    url=referrer,
                                                    path=referrer_type,
                                                    **account_details)
            else:
                SubscriptionReferrer.create(created_on=created_on,
                                            url=referrer,
                                            type=referrer_type,
                                            **account_details)

        marketing_survey_answer = csv_row['Jak ses dozvěděl(a) o junior.guru?'] or None
        if marketing_survey_answer:
            marketing_survey_answer_type = classify_marketing_survey_answer(marketing_survey_answer)
            SubscriptionMarketingSurvey.create(account_id=account_id,
                                               account_name=csv_row['Full Name'],
                                               account_email=csv_row['Email'],
                                               account_total_spend=total_spend[account_id],
                                               created_on=date.fromisoformat(csv_row['Created at']),
                                               value=marketing_survey_answer,
                                               type=marketing_survey_answer_type)

    logger.info("Fetching cancellations data from Memberful CSV")
    csv_rows = itertools.chain(memberful.download_csv(dict(type='CancellationsCsvExport', filter='all')),
                               memberful.download_csv(dict(type='CancellationsCsvExport', scope='completed', filter='all')))
    for csv_row in csv_rows:
        reason = slugify(csv_row['Reason'], separator='_') if csv_row['Reason'] else None
        feedback = csv_row['Feedback'] or None
        if reason:
            try:
                date_field_value = csv_row.get('Date') or csv_row.get('Expiration Date')
                expires_on = date.fromisoformat(date_field_value)
            except ValueError:
                logger.warning(f"Invalid date format: {date_field_value!r}")
                expires_on = None
            account_email = csv_row['Email']
            account_id = emails[account_email]
            SubscriptionCancellation.create(account_id=account_id,
                                            account_name=csv_row['Name'],
                                            account_email=account_email,
                                            account_total_spend=total_spend[account_id],
                                            expires_on=expires_on,
                                            reason=reason,
                                            feedback=feedback)


def classify_referrer(url: str) -> str:
    parts = urlparse(url)
    if parts.netloc == 'junior.guru':
        return parts.path.rstrip('/') or '/'
    if parts.netloc == 't.co':
        return 'twitter'
    if parts.netloc == 'honzajavorek.cz':
        return 'honzajavorek'
    domain = parts.netloc.split('.')[-2]
    if domain in ('google', 'facebook', 'linkedin', 'youtube'):
        return domain
    return 'other'


def classify_marketing_survey_answer(text: str) -> str:
    text = text.strip()
    if re.search(r'\b(yablk\w+|rob\s*web)\b', text, re.I):
        return 'yablko'
    if re.search(r'\b(pod[ck][aá]st\w*|spotify|rozbité prasátko|Street ?of ?Code)\b', text, re.I):
        return 'podcasts'
    if re.search(r'\brecenz\w+\b', text, re.I):
        return 'courses_search'
    if re.search(r'\bpyladies\b', text, re.I):
        return 'courses'
    if re.search(r'\bczechitas\b', text, re.I):
        return 'courses'
    if (re.search(r'\b(software\s+development\s+academy|sd\s*academy|sda\s+academy)\b', text, re.I) or
        re.search(r'\bSDA\b', text)):
        return 'courses'
    if re.search(r'\b(kurz\w*|akademie|enget\w*|green\s*fox\w*|it\s*network\w*|webin[áa][řr]\w*)\b', text, re.I):
        return 'courses'
    if re.search(r'\b(youtube|yt)\b', text, re.I):
        return 'youtube'
    if re.search(r'\b(facebook\w*|fb|fcb)\b', text, re.I):
        return 'facebook'
    if (re.search(r'\blinkedin\w*\b', text, re.I) or
        re.search(r'\bLI\b', text)):
        return 'linkedin'
    if re.search(r'\b(goo?gl\w*|vyhled[aá]v\w+)\b', text, re.I):
        return 'search'
    if re.search(r'\b(komunit\w+|kamar[aá]d\w*|brat\w*|koleg\w*|br[aá]ch\w*|manžel\w*|partner\w*|p[řr][íi]a?tel\w*|přátelé|pratele|zn[áa]m[ée]\w*|doporu[čc]en\w+|Skládanka|Stan\w+ Prokop\w*|Tom\w* Hrn\w*)\b', text, re.I):
        return 'friend'
    if re.search(r'^od\s+\w{3,}', text.strip(), re.I):
        return 'friend'
    if re.search(r'\b(\w*hled[aá]\w+|h[ľl]ad[aá]\w+|search|na[šs]la|na[šs]i?el)\b', text, re.I):
        return 'search'
    if re.search(r'\binternet\w?\b', text, re.I):
        return 'internet'
    if re.search(r'^(net\w?|web\w?|online)$', text, re.I):
        return 'internet'
    if re.search(r'^\b\w{1,2}\s+(internet|web|net)\w*$', text, re.I):
        return 'internet'
    return 'other'
