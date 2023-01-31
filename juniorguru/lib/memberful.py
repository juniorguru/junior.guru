import json
import os
from string import Template

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from juniorguru.lib import loggers


MEMBERFUL_API_KEY = os.environ['MEMBERFUL_API_KEY']

MEMBERFUL_MUTATIONS_ENABLED = bool(int(os.getenv('MEMBERFUL_MUTATIONS_ENABLED', 0)))


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
                                              headers={'Authorization': f'Bearer {self.api_key}'},
                                              verify=True, retries=3)
            self._client = Client(transport=transport)
        return self._client

    def _query(self, gql_query, get_page_info):
        cursor = ''
        query_gql = gql(gql_query)
        while cursor is not None:
            logger.debug('Sending a query')
            params = dict(cursor=cursor)
            result = self.client.execute(query_gql, variable_values=params)
            yield result
            page_info = get_page_info(result)
            if page_info['hasNextPage']:
                cursor = page_info['endCursor']
            else:
                cursor = None

    def get_nodes(self, collection_name, gql_fields):
        # way too many brackets for f-strings, using template
        # requires only to have $$cursor instead of $cursor
        gql_query_template = Template("""
            query getNodes($$cursor: String!) {
                $collection_name(after: $$cursor) {
                    totalCount
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                    edges {
                        node {
                            $gql_fields
                        }
                    }
                }
            }
        """)
        gql_query = gql_query_template.substitute(collection_name=collection_name,
                                                  gql_fields=gql_fields)
        get_page_info = lambda result: result[collection_name]['pageInfo']
        for result in self._query(gql_query, get_page_info):
            for edge in result[collection_name]['edges']:
                yield edge['node']

    def mutate(self, mutation_string, params):
        logger.debug('Sending a mutation')
        self.client.execute(gql(mutation_string), variable_values=params)


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


def get_nodes(collection_name, graphql_results):
    for grapqhql_result in graphql_results:
        for edge in grapqhql_result[collection_name]['edges']:
            yield edge['node']
