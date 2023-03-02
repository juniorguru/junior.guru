import os
import re
from datetime import date, datetime
import html
from decimal import Decimal
from pprint import pformat

import requests
import click
from fiobank import FioBank

from juniorguru.cli.sync import main as cli
from juniorguru.lib import google_sheets, loggers
from juniorguru.lib.google_sheets import GOOGLE_SHEETS_MUTATIONS_ENABLED
from juniorguru.models.transaction import Transaction


FAKTUROID_MUTATIONS_ENABLED = bool(int(os.getenv('FAKTUROID_MUTATIONS_ENABLED', 0)))

TODO_TEXT_RE = re.compile(r'''
    ^
        Nespárovaná\s+
        příchozí\s+
        platba[\s\-]+
        VS:\s+
        (?P<variable_symbol>\w+)?,\s+
        částka:\s+
        (?P<amount>[\d\xa0,]+)\s+
    Kč
''', re.VERBOSE)

CATEGORIES = [
    lambda t: 'memberships' if t['variable_symbol'] in ['21', '243', '241'] else None,
    lambda t: 'memberships' if t['variable_symbol'] == '215' else None,
    lambda t: 'partnerships' if 'SKLIK' in t['message'] and 'SEZNAM' in t['message'] else None,
    lambda t: 'partnerships' if t['variable_symbol'] == '226' else None,
    lambda t: 'salary' if 'výplata' in t['message'] else None,
    lambda t: 'sideline' if t['variable_symbol'] == '15' else None,
    lambda t: 'video' if os.environ['VIDEO_OUTSOURCING_TOKEN'] in t['message'] else None,
    lambda t: 'podcast' if 'PAVLINA FRONKOVA' in t['message'] else None,
    lambda t: 'lawyer' if 'ADVOKATKA' in t['message'] else None,
    lambda t: 'marketing' if 'JANA DOLEJSOVA' in t['message'] else None,
    lambda t: 'accounting' if 'Irein' in t['message'] else None,
    lambda t: 'accounting' if 'účetnictví' in t['message'] else None,
    lambda t: 'fakturoid' if 'účetnictví' in t['message'] and t['amount'] < 0 else None,
    lambda t: 'discord' if 'DISCORD' in t['message'] and t['amount'] < 0 else None,
    lambda t: 'memberful' if 'MEMBERFUL' in t['message'] and t['amount'] < 0 else None,
    lambda t: 'partnerships' if 'RED HAT' in t['message'] and t['amount'] >= 8000 else None,
    lambda t: 'tax' if ('ČSSZ' in t['message'] or 'PSSZ' in t['message'] or 'MSSZ' in t['message']) else None,
    lambda t: 'tax' if 'VZP' in t['message'] else None,
    lambda t: 'tax' if 'FÚ pro hl. m. Prahu' in t['message'] else None,
    lambda t: 'marketing' if 'BUFFER PUBLISH' in t['message'] and t['amount'] < 0 else None,
    lambda t: 'marketing' if 'PrintAll' in t['message'] and t['amount'] < 0 else None,
    lambda t: 'marketing' if 'samolep' in t['message'] and t['amount'] < 0 else None,
    lambda t: 'donations' if 'GITHUB SPONSORS' in t['message'] and t['amount'] > 0 else None,
    lambda t: 'memberships' if 'STRIPE' in t['message'] and t['amount'] > 0 else None,
    lambda t: 'donations' if 'PAYPAL' in t['message'] and t['amount'] > 0 else None,
    lambda t: 'donations' if not t['variable_symbol'] and t['amount'] > 0 else None,
    lambda t: 'donations' if t['variable_symbol'] == '444222' and t['amount'] > 0 else None,
    lambda t: 'partnerships' if t['variable_symbol'] and t['amount'] >= 8000 else None,
    lambda t: 'jobs' if t['variable_symbol'] and t['amount'] > 0 else None,
    lambda t: 'donations' if t['amount'] > 0 else 'miscellaneous',
]

TOGGLE_TODOS_CATEGORIES = [
    'donations',
    'memberships',
]


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option('--from-date', default='2020-01-01', type=date.fromisoformat)
@click.option('--fio-api-key', default=lambda: os.environ['FIOBANK_API_KEY'])
@click.option('--fakturoid-api-base-url', default='https://app.fakturoid.cz/api/v2/accounts/honzajavorek')
@click.option('--fakturoid-api-key', default=lambda: os.environ['FAKTUROID_API_KEY'])
@click.option('--doc-key', default='1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls')
def main(from_date, fio_api_key, fakturoid_api_base_url, fakturoid_api_key, doc_key):
    fakturoid_api_kwargs = dict(auth=('mail@honzajavorek.cz', fakturoid_api_key),
                                headers={'User-Agent': 'JuniorGuruBot (honza@junior.guru; +https://junior.guru)'})

    logger.info('Preparing database')
    Transaction.drop_table()
    Transaction.create_table()

    logger.info('Getting Fakturoid todos for unpaired transactions')
    todos = []
    page = 1
    while True:
        logger.debug(f'Fakturoid todos, page {page}')
        response = requests.get(f'{fakturoid_api_base_url}/todos.json',
                                params=dict(page=page), **fakturoid_api_kwargs)
        response.raise_for_status()
        todos.extend(todo for todo
                     in response.json()
                     if (todo['name'] == 'invoice_payment_unpaired'
                         and not todo['completed_at']))
        if 'rel="last"' not in response.headers['Link']:
            break
        page += 1
    logger.info(f'Found {len(todos)} Fakturoid todos')
    todos = {get_todo_key(todo): todo for todo in todos}
    logger.debug(f'Mapping Fakturoid todos by key leaves {len(todos)} todos')

    logger.info('Reading data from the bank account')
    client = FioBank(token=fio_api_key)
    from_date = from_date.strftime('%Y-%m-%d')
    to_date = date.today().strftime('%Y-%m-%d')
    transactions = client.period(from_date=from_date, to_date=to_date)

    db_records = []
    doc_records = []
    todos_to_toggle = []
    for transaction in transactions:
        transaction_key = get_transaction_key(transaction)
        logger.debug(f"Transaction key: {transaction_key!r}")
        if transaction['currency'].upper() != 'CZK':
            raise ValueError(f"Unexpected currency: {transaction['currency']}")
        message = get_transaction_message(transaction)
        logger.debug(f"Message: {message!r}")
        category = get_transaction_category(dict(message=message, **transaction))
        logger.debug(f"Category: {category!r}")

        db_records.append(dict(happened_on=transaction['date'],
                               category=category,
                               amount=transaction['amount']))
        doc_records.append({
            'Date': transaction['date'].strftime('%Y-%m-%d'),
            'Category': category,
            'Amount': transaction['amount'],
            'Message': message,
            'Variable Symbol': transaction['variable_symbol'],
        })

        if category in TOGGLE_TODOS_CATEGORIES and (todo := todos.get(transaction_key)):
            logger.info(f"Found todo to toggle: ID {todo['id']}, {get_todo_key(todo)}")
            logger.debug(f"Todo: {pformat(todo)}")
            todos_to_toggle.append(todo)

    logger.info('Saving essential data to the database')
    for db_record in db_records:
        Transaction.create(**db_record)

    logger.info('Uploading verbose data to a private Google Sheet for manual audit of possible mistakes')
    if GOOGLE_SHEETS_MUTATIONS_ENABLED:
        google_sheets.upload(google_sheets.get(doc_key, 'transactions'), doc_records)
    else:
        logger.warning('Google Sheets mutations not enabled')

    logger.info(f'Toggling {len(todos_to_toggle)} Fakturoid todos')
    if FAKTUROID_MUTATIONS_ENABLED:
        for todo in todos_to_toggle:
            todo_id = todo['id']
            logger.info(f"Toggling todo: ID {todo_id}")
            response = requests.post(f'{fakturoid_api_base_url}/todos/{todo_id}/toggle_completion.json',
                                    **fakturoid_api_kwargs)
            response.raise_for_status()
    else:
        logger.warning('Fakturoid mutations not enabled')


def get_transaction_message(transaction):
    return ', '.join(filter(None, [
        transaction.get('comment'),
        transaction.get('user_identification'),
        transaction.get('recipient_message'),
    ]))


def get_transaction_category(transaction):
    for category_fn in CATEGORIES:
        category = category_fn(transaction)
        if category:
            return category
    raise ValueError('Could not categorize transaction')


def get_transaction_key(transaction):
    return (transaction['date'],
            transaction['variable_symbol'],
            Decimal(transaction['amount']))


def get_todo_key(todo):
    parse_result = parse_todo_text(todo['text'])
    return (datetime.fromisoformat(todo['created_at']).date(),
            parse_result['variable_symbol'],
            parse_result['amount'])


def parse_todo_text(text):
    text = html.unescape(text)
    match = TODO_TEXT_RE.search(text)
    parse_result = match.groupdict()
    if parse_result['variable_symbol'] == '0':
        variable_symbol = None
    else:
        variable_symbol = parse_result['variable_symbol']
    amount = Decimal(parse_result['amount'].replace('\xa0', '').replace(',', '.'))
    return dict(variable_symbol=variable_symbol, amount=amount)
