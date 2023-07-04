import json
import os
import re
from typing import Callable

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from juniorguru.lib import loggers


COLLECTION_NAME_RE = re.compile(r'(?P<collection_name>\w+)\(after:\s*\$cursor')

MEMBERFUL_API_KEY = os.environ['MEMBERFUL_API_KEY']


logger = loggers.from_path(__file__)


class Memberful():
    # https://memberful.com/help/integrate/advanced/memberful-api/
    # https://juniorguru.memberful.com/api/graphql/explorer?api_user_id=52463

    def __init__(self, api_key=None):
        self.api_key = api_key or MEMBERFUL_API_KEY
        self._client = None

    @property
    def client(self):
        if not self._client:
            logger.debug('Connecting')
            transport = RequestsHTTPTransport(url='https://juniorguru.memberful.com/api/graphql/',
                                              headers={'Authorization': f'Bearer {self.api_key}',
                                                       'User-Agent': 'JuniorGuruBot (+https://junior.guru)'},
                                              verify=True,
                                              retries=3)
            self._client = Client(transport=transport)
        return self._client

    def _query(self, query: str, get_page_info: Callable, variable_values: dict=None):
        variable_values = variable_values or {}
        cursor = ''
        query_gql = gql(query)
        while cursor is not None:
            logger.debug('Sending a query')
            result = self.client.execute(query_gql,
                                         variable_values=dict(cursor=cursor, **variable_values))
            yield result
            page_info = get_page_info(result)
            if page_info['hasNextPage']:
                cursor = page_info['endCursor']
            else:
                cursor = None

    def get_nodes(self, query: str, variable_values: dict=None):
        if match := COLLECTION_NAME_RE.search(query):
            collection_name = match.group('collection_name')
        else:
            raise ValueError('Could not parse collection name')
        for result in self._query(query,
                                  lambda result: result[collection_name]['pageInfo'],
                                  variable_values):
            for edge in result[collection_name]['edges']:
                yield edge['node']

    def mutate(self, mutation: str, variable_values: dict):
        logger.debug('Sending a mutation')
        return self.client.execute(gql(mutation), variable_values=variable_values)


def serialize_metadata(data):
    # https://memberful.com/help/custom-development-and-api/memberful-api/#member-metadata
    if len(data) > 500:
        raise ValueError('Maximum 50 keys')
    for key, value in data.items():
        if len(key) > 40:
            raise ValueError(f"Maximum key length is 40 characters: {key!r}")
        if value is None:
            raise TypeError("If you want to unset value, use empty string, not None")
        if not isinstance(value, str):
            raise TypeError(f"Limited to string values! {value!r}")
        if len(value) > 500:
            raise ValueError(f"Maximum value length is 500 characters: {value!r}")
    return json.dumps(data)
