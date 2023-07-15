import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Callable, Generator

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from juniorguru.lib import loggers


COLLECTION_NAME_RE = re.compile(r'(?P<collection_name>\w+)\(after:\s*\$cursor')

MEMBERFUL_API_KEY = os.environ['MEMBERFUL_API_KEY']


logger = loggers.from_path(__file__)


class Memberful():
    # https://memberful.com/help/integrate/advanced/memberful-api/
    # https://juniorguru.memberful.com/api/graphql/explorer?api_user_id=52463

    def __init__(self, api_key: str=None, cache_dir: str|Path=None, clear_cache: bool=False):
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.clear_cache = clear_cache
        self.api_key = api_key or MEMBERFUL_API_KEY
        self._client = None

    @property
    def client(self) -> Client:
        if not self._client:
            logger.debug('Connecting')
            transport = RequestsHTTPTransport(url='https://juniorguru.memberful.com/api/graphql/',
                                              headers={'Authorization': f'Bearer {self.api_key}',
                                                       'User-Agent': 'JuniorGuruBot (+https://junior.guru)'},
                                              verify=True,
                                              retries=3)
            self._client = Client(transport=transport)
        return self._client

    def mutate(self, mutation: str, variable_values: dict) -> dict[str, Any]:
        logger.debug('Sending a mutation')
        return self.client.execute(gql(mutation), variable_values=variable_values)

    def get_nodes(self, query: str, variable_values: dict=None) -> Generator[dict, None, None]:
        if match := COLLECTION_NAME_RE.search(query):
            collection_name = match.group('collection_name')
        else:
            raise ValueError('Could not parse collection name')
        declared_count = None
        nodes_count = 0
        duplicates_count = 0
        seen_node_ids = set()
        for result in self._query(query,
                                  lambda result: result[collection_name]['pageInfo'],
                                  variable_values=variable_values):
            # save total count so we can later check if we got all the nodes
            count = result[collection_name]['totalCount']
            if declared_count is None:
                logger.debug(f'Expecting {count} nodes')
                declared_count = count
            assert declared_count == count, f'Memberful API suddenly declares different total count: {count} (≠ {declared_count})'

            # iterate over nodes and drop duplicates, because, unfortunately, the API returns duplicates
            for edge in result[collection_name]['edges']:
                node = edge['node']
                node_id = node.get('id') or hash_data(node)
                if node_id in seen_node_ids:
                    logger.debug(f'Dropping a duplicate node: {node_id!r}')
                    duplicates_count += 1
                else:
                    yield node
                    seen_node_ids.add(node_id)
                nodes_count += 1
        assert duplicates_count == 0, f'Memberful API returned {duplicates_count} duplicate nodes'
        assert declared_count == nodes_count, f"Memberful API returned {nodes_count} nodes instead of {declared_count}"

    def _query(self, query: str, get_page_info: Callable, variable_values: dict=None):
        variable_values = variable_values or {}
        cursor = ''
        n = 0
        while cursor is not None:
            logger.debug(f'Sending a query with cursor {cursor!r}')
            result = self._execute_query(query, dict(cursor=cursor, **variable_values))
            yield result
            n += 1
            page_info = get_page_info(result)
            if page_info['hasNextPage']:
                cursor = page_info['endCursor']
            else:
                cursor = None

    def _execute_query(self, query: str, variable_values: dict) -> dict:
        if self.cache_dir:
            if self.clear_cache:
                logger.debug('Clearing cache')
                for path in self.cache_dir.glob('memberful-*.json'):
                    path.unlink()
                self.clear_cache = False

            cache_key = hash_data(dict(query=query, variable_values=variable_values))
            cache_path = self.cache_dir / f'memberful-{cache_key}.json'
            try:
                with cache_path.open() as f:
                    logger.debug(f'Loading from cache: {cache_path}')
                    return json.load(f)
            except FileNotFoundError:
                pass

        logger.debug('Querying Memberful API')
        result = self.client.execute(gql(query), variable_values=variable_values)

        if self.cache_dir:
            logger.debug(f'Saving to cache: {cache_path}')
            with cache_path.open('w') as f:
                json.dump(result, f)

        return result


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


def hash_data(data: dict) -> str:
    return hashlib.sha256(json.dumps(data).encode()).hexdigest()
