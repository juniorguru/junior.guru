import base64
import html
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from pprint import pformat
from typing import Callable

import click
import requests
from fiobank import FioBank

from jg.coop.cli.sync import confirm, default_from_env, main as cli
from jg.coop.lib import loggers, mutations
from jg.coop.models.transaction import Transaction, TransactionsCategory
from jg.coop.sync.transactions.categories_spec import CATEGORIES_SPEC


FAKTUROID_API_USER_AGENT = "JuniorGuruBot (honza@junior.guru; +https://junior.guru)"

TODO_TEXT_RE = re.compile(
    r"""
        ^
            Nespárovaná\s+
            příchozí\s+
            platba[\s\-]+
            VS:\s+
            (?P<variable_symbol>\w+)?,\s+
            částka:\s+
            (?P<amount>[\d\xa0,]+)\s+
        Kč
    """,
    re.VERBOSE,
)

TOGGLE_TODOS_CATEGORIES = [
    TransactionsCategory.DONATIONS,
    TransactionsCategory.MEMBERSHIPS,
    TransactionsCategory.TAX,
]


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option("--from-date", default="2020-01-01", type=date.fromisoformat)
@click.option("--fio-api-key", default=default_from_env("FIOBANK_API_KEY"))
@click.option(
    "--fakturoid-api-base-url",
    default="https://app.fakturoid.cz/api/v3/accounts/honzajavorek",
)
@click.option("--fakturoid-client-id", default=default_from_env("FAKTUROID_CLIENT_ID"))
@click.option(
    "--fakturoid-client-secret", default=default_from_env("FAKTUROID_CLIENT_SECRET")
)
@click.option(
    "--video-outsourcing-token", default=default_from_env("VIDEO_OUTSOURCING_TOKEN")
)
@click.option(
    "--history-path",
    default="jg/coop/data/transactions.jsonl",
    type=click.Path(exists=True, path_type=Path),
)
@click.option("--clear-history/--keep-history", default=False)
def main(
    from_date,
    fio_api_key,
    fakturoid_api_base_url,
    fakturoid_client_id,
    fakturoid_client_secret,
    video_outsourcing_token,
    history_path,
    clear_history,
):
    logger.info("Getting Fakturoid API token")
    credentials = f"{fakturoid_client_id}:{fakturoid_client_secret}"
    credentials_base64 = base64.b64encode(credentials.encode()).decode()
    response = requests.post(
        "https://app.fakturoid.cz/api/v3/oauth/token",
        headers={
            "Accept": "application/json",
            "User-Agent": FAKTUROID_API_USER_AGENT,
            "Authorization": f"Basic {credentials_base64}",
        },
        json=dict(grant_type="client_credentials"),
    )
    response.raise_for_status()
    fakturoid_token = response.json()["access_token"]

    logger.info("Preparing categories")
    categories_spec = CATEGORIES_SPEC
    if not video_outsourcing_token:
        logger.warning(
            "No --video-outsourcing-token! Transactions won't be categorized correctly"
        )
        if not confirm("Continue anyway?"):
            raise click.Abort()
    secrets = dict(video_outsourcing_token=video_outsourcing_token)

    logger.info("Preparing database")
    Transaction.drop_table()
    Transaction.create_table()

    logger.info("Getting Fakturoid todos for unpaired transactions")
    todos = []
    page = 1
    while True:
        logger.debug(f"Fakturoid todos, page {page}")
        response = requests.get(
            f"{fakturoid_api_base_url}/todos.json",
            params=dict(page=page),
            headers={
                "User-Agent": FAKTUROID_API_USER_AGENT,
                "Authorization": f"Bearer {fakturoid_token}",
            },
        )
        response.raise_for_status()
        todos_page = response.json()
        todos.extend(
            todo
            for todo in todos_page
            if (todo["name"] == "invoice_payment_unpaired" and not todo["completed_at"])
        )
        if not todos_page:
            break
        page += 1
    logger.info(f"Found {len(todos)} Fakturoid todos")
    todos = {get_todo_key(todo): todo for todo in todos}
    logger.debug(f"Mapping Fakturoid todos by key leaves {len(todos)} todos")
    for key in todos.keys():
        logger.debug(f"Todo key: {key!r}")

    logger.info("Reading history from a file")
    if clear_history:
        history_path.write_text("")
    else:
        with history_path.open() as f:
            for line in f:
                Transaction.deserialize(line)

    to_date = date.today()
    from_date = min(
        Transaction.history_end_on() or from_date,
        to_date - timedelta(days=14),
    )
    logger.info(f"Reading data from the bank account, since {from_date}")
    client = FioBank(token=fio_api_key)
    try:
        transactions = list(
            client.period(from_date=str(from_date), to_date=str(to_date))
        )
    except requests.HTTPError as e:
        logger.error(f"FioBank API error: {e.response.text}")
        raise e
    except requests.ConnectionError:
        logger.error("FioBank API connection error!")
        transactions = []

    db_records = []
    todos_to_toggle = {}
    for transaction in transactions:
        transaction_key = get_transaction_key(transaction)
        logger.debug(f"Transaction key: {transaction_key!r}")
        if transaction["currency"].upper() != "CZK":
            raise ValueError(f"Unexpected currency: {transaction['currency']}")
        message = get_transaction_message(transaction)
        logger.debug(f"Message: {message!r}")
        category = get_transaction_category(
            dict(message=message, **transaction), categories_spec, secrets
        )
        logger.debug(f"Category: {category!r}")
        if category != TransactionsCategory.IGNORE:
            db_records.append(
                dict(
                    id=transaction["transaction_id"],
                    happened_on=transaction["date"],
                    category=category,
                    amount=transaction["amount"],
                )
            )
        if (
            transaction["amount"] > 0
            and category in TOGGLE_TODOS_CATEGORIES
            and (todo := todos.get(transaction_key))
        ):
            logger.info(f"Found todo to toggle: ID {todo['id']}, {get_todo_key(todo)}")
            logger.debug(f"Todo: {pformat(todo)}")
            # Using dict to prevent double toggle for todos matching more transactions
            todos_to_toggle[todo["id"]] = todo

    logger.info("Saving essential data to the database")
    for db_record in db_records:
        Transaction.add(**db_record)

    logger.info("Saving history to a file")
    with history_path.open("w") as f:
        for db_object in Transaction.history():
            f.write(db_object.serialize())

    logger.info(f"Toggling {len(todos_to_toggle)} Fakturoid todos")
    for todo in todos_to_toggle.values():
        toggle_fakturoid_todo(fakturoid_api_base_url, fakturoid_token, todo["id"])


@mutations.mutates_fakturoid()
def toggle_fakturoid_todo(api_base_url: str, api_token: str, todo_id: int):
    logger.info(f"Toggling todo: ID {todo_id}")
    response = requests.post(
        f"{api_base_url}/todos/{todo_id}/toggle_completion.json",
        headers={
            "User-Agent": FAKTUROID_API_USER_AGENT,
            "Authorization": f"Bearer {api_token}",
        },
    )
    response.raise_for_status()


def get_transaction_message(transaction):
    return ", ".join(
        filter(
            None,
            [
                transaction.get("comment"),
                transaction.get("user_identification"),
                transaction.get("recipient_message"),
            ],
        )
    )


def get_transaction_category(
    transaction: dict, categories_spec: list[Callable], secrets: dict
) -> TransactionsCategory:
    for category_rule in categories_spec:
        category = category_rule(transaction, secrets)
        if category:
            return category
    raise ValueError("Could not categorize transaction")


def get_transaction_key(transaction):
    return (
        transaction["date"],
        normalize_variable_symbol(transaction["variable_symbol"]),
        transaction["amount"],
    )


def get_todo_key(todo):
    parse_result = parse_todo_text(todo["text"])
    return (
        datetime.fromisoformat(todo["created_at"]).date(),
        normalize_variable_symbol(parse_result["variable_symbol"]),
        parse_result["amount"],
    )


def parse_todo_text(text):
    text = html.unescape(text)
    match = TODO_TEXT_RE.search(text)
    parse_result = match.groupdict()
    amount = float(parse_result["amount"].replace("\xa0", "").replace(",", "."))
    return dict(variable_symbol=parse_result["variable_symbol"], amount=amount)


def normalize_variable_symbol(variable_symbol):
    if not variable_symbol:
        return None
    if variable_symbol == "0":
        return None
    return variable_symbol
