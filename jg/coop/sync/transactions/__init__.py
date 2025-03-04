import re
from datetime import date, datetime, timedelta
from pathlib import Path
from pprint import pformat
from typing import Callable

import click
import httpx
import requests
from fiobank import FioBank

from jg.coop.cli.sync import confirm, default_from_env, main as cli
from jg.coop.lib import fakturoid, loggers, mutations
from jg.coop.models.transaction import Transaction, TransactionsCategory
from jg.coop.sync.transactions.categories_spec import CATEGORIES_SPEC


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
@click.option(
    "--from-date",
    default="2020-01-01",
    type=date.fromisoformat,
    required=True,
)
@click.option(
    "--fio-api-key",
    default=default_from_env("FIOBANK_API_KEY"),
    required=True,
)
@click.option(
    "--video-outsourcing-token",
    default=default_from_env("VIDEO_OUTSOURCING_TOKEN"),
    required=False,
)
@click.option(
    "--history-path",
    default="jg/coop/data/transactions.jsonl",
    type=click.Path(exists=True, path_type=Path),
    required=True,
)
@click.option("--clear-history/--keep-history", default=False)
def main(
    from_date: str,
    fio_api_key: str,
    video_outsourcing_token: str | None,
    history_path: Path,
    clear_history: bool,
):
    logger.info("Getting Fakturoid API token")
    fakturoid_token = fakturoid.auth()

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
    with fakturoid.get_client(fakturoid_token) as client:
        while True:
            logger.debug(f"Fakturoid todos, page {page}")
            response = client.get("/todos.json", params=dict(page=page))
            response.raise_for_status()
            todos_page = response.json()
            todos.extend(
                todo
                for todo in todos_page
                if (
                    todo["name"] == "invoice_payment_unpaired"
                    and not todo["completed_at"]
                )
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
    with fakturoid.get_client(fakturoid_token) as client:
        for todo in todos_to_toggle.values():
            toggle_fakturoid_todo(client, todo["id"])


@mutations.mutates_fakturoid()
def toggle_fakturoid_todo(client: httpx.Client, todo_id: int):
    logger.info(f"Toggling todo: ID {todo_id}")
    response = client.post(f"/todos/{todo_id}/toggle_completion.json")
    response.raise_for_status()


def get_transaction_message(transaction: dict) -> str:
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


def get_transaction_key(transaction) -> tuple[date, str | None, float]:
    return (
        transaction["date"],
        normalize_variable_symbol(transaction["variable_symbol"]),
        transaction["amount"],
    )


def get_todo_key(todo: dict) -> tuple[date, str | None, float]:
    return (
        datetime.fromisoformat(todo["created_at"]).date(),
        normalize_variable_symbol(todo["params"]["variable_symbol"]),
        float(todo["params"]["amount"]),
    )


def normalize_variable_symbol(variable_symbol: str) -> str | None:
    if not variable_symbol:
        return None
    if variable_symbol == "0":
        return None
    return variable_symbol
