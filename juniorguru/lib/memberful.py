import hashlib
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
        n = 0
        while cursor is not None:
            logger.debug(f'Sending a query with cursor {cursor!r}')
            result = self.client.execute(query_gql,
                                         variable_values=dict(cursor=cursor, **variable_values))
            yield result
            n += 1
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
        declared_count = None
        nodes_count = 0
        seen_node_ids = set()
        for result in self._query(query,
                                  lambda result: result[collection_name]['pageInfo'],
                                  variable_values=variable_values):
            # save total count so we can later check if we got all the nodes
            count = result[collection_name]['totalCount']
            if declared_count is None:
                declared_count = count
            assert declared_count == count, f'Memberful API suddenly declares different total count: {count} (≠ {declared_count})'

            # iterate over nodes and drop duplicates, because, unfortunately, the API returns duplicates
            for edge in result[collection_name]['edges']:
                node = edge['node']
                node_id = node.get('id') or hashlib.sha256(json.dumps(node).encode()).hexdigest()
                if node_id in seen_node_ids:
                    logger.debug(f'Dropping a duplicate node: {node_id!r}')
                else:
                    yield node
                    seen_node_ids.add(node_id)
                nodes_count += 1
        assert declared_count == nodes_count, f"Memberful API returned {nodes_count} nodes instead of {declared_count}"

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
