import html
import re
from datetime import date, datetime
from pprint import pformat

import click
import requests
from fiobank import FioBank

from juniorguru.cli.sync import confirm, default_from_env, main as cli
from juniorguru.lib import google_sheets, loggers, mutations
from juniorguru.models.transaction import Transaction


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

CATEGORIES_SPEC = [
    lambda t: 'memberships' if t['variable_symbol'] in ['21', '243', '241'] else None,
    lambda t: 'memberships' if t['variable_symbol'] == '215' else None,
    lambda t: 'partnerships' if 'SKLIK' in t['message'] and 'SEZNAM' in t['message'] else None,
    lambda t: 'partnerships' if t['variable_symbol'] == '226' else None,
    lambda t: 'salary' if 'výplata' in t['message'] else None,
    lambda t: 'sideline' if t['variable_symbol'] == '15' else None,
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
    'tax',
]


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option('--from-date', default='2020-01-01', type=date.fromisoformat)
@click.option('--fio-api-key', default=default_from_env('FIOBANK_API_KEY'))
@click.option('--fakturoid-api-base-url', default='https://app.fakturoid.cz/api/v2/accounts/honzajavorek')
@click.option('--fakturoid-api-key', default=default_from_env('FAKTUROID_API_KEY'))
@click.option('--doc-key', default='1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls')
@click.option('--video-outsourcing-token', default=default_from_env('VIDEO_OUTSOURCING_TOKEN'))
def main(from_date, fio_api_key, fakturoid_api_base_url, fakturoid_api_key, doc_key,
         video_outsourcing_token):
    fakturoid_api_kwargs = dict(auth=('mail@honzajavorek.cz', fakturoid_api_key),
                                headers={'User-Agent': 'JuniorGuruBot (honza@junior.guru; +https://junior.guru)'})

    logger.info('Preparing categories')
    categories_spec = list(CATEGORIES_SPEC)
    if video_outsourcing_token:
        video_category_spec = lambda t: 'video' if video_outsourcing_token in t['message'] else None
        categories_spec.insert(0, video_category_spec)
    else:
        logger.warning("No --video-outsourcing-token! Transactions won't be categorized correctly")
        if not confirm('Continue anyway?'):
            raise click.Abort()

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
    todos_to_toggle = {}
    for transaction in transactions:
        transaction_key = get_transaction_key(transaction)
        logger.debug(f"Transaction key: {transaction_key!r}")
        if transaction['currency'].upper() != 'CZK':
            raise ValueError(f"Unexpected currency: {transaction['currency']}")
        message = get_transaction_message(transaction)
        logger.debug(f"Message: {message!r}")
        category = get_transaction_category(dict(message=message, **transaction),
                                            categories_spec)
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

        if (
            transaction['amount'] > 0
            and category in TOGGLE_TODOS_CATEGORIES
            and (todo := todos.get(transaction_key))
        ):
            logger.info(f"Found todo to toggle: ID {todo['id']}, {get_todo_key(todo)}")
            logger.debug(f"Todo: {pformat(todo)}")
            todos_to_toggle[todo['id']] = todo  # using dict to prevent double toggle for todos matching more transactions

    logger.info('Saving essential data to the database')
    for db_record in db_records:
        Transaction.create(**db_record)

    logger.info('Uploading verbose data to a private Google Sheet for manual audit of possible mistakes')
    upload_to_google_sheet(doc_key, doc_records)

    logger.info(f'Toggling {len(todos_to_toggle)} Fakturoid todos')
    for todo in todos_to_toggle.values():
        toggle_fakturoid_todo(fakturoid_api_base_url, fakturoid_api_kwargs, todo)


@mutations.mutates('google_sheets')
def upload_to_google_sheet(doc_key, doc_records):
    google_sheets.upload(google_sheets.get(doc_key, 'transactions'), doc_records)


@mutations.mutates('fakturoid')
def toggle_fakturoid_todo(api_base_url, api_kwargs, todo):
    todo_id = todo['id']
    logger.info(f"Toggling todo: ID {todo_id}")
    response = requests.post(f'{api_base_url}/todos/{todo_id}/toggle_completion.json',
                                **api_kwargs)
    response.raise_for_status()


def get_transaction_message(transaction):
    return ', '.join(filter(None, [
        transaction.get('comment'),
        transaction.get('user_identification'),
        transaction.get('recipient_message'),
    ]))


def get_transaction_category(transaction, categories_spec):
    for category_fn in categories_spec:
        category = category_fn(transaction)
        if category:
            return category
    raise ValueError('Could not categorize transaction')


def get_transaction_key(transaction):
    return (transaction['date'],
            normalize_variable_symbol(transaction['variable_symbol']),
            transaction['amount'])


def get_todo_key(todo):
    parse_result = parse_todo_text(todo['text'])
    return (datetime.fromisoformat(todo['created_at']).date(),
            normalize_variable_symbol(parse_result['variable_symbol']),
            parse_result['amount'])


def parse_todo_text(text):
    text = html.unescape(text)
    match = TODO_TEXT_RE.search(text)
    parse_result = match.groupdict()
    amount = float(parse_result['amount'].replace('\xa0', '').replace(',', '.'))
    return dict(variable_symbol=parse_result['variable_symbol'], amount=amount)


def normalize_variable_symbol(variable_symbol):
    if not variable_symbol:
        return None
    if variable_symbol == '0':
        return None
    return variable_symbol
