import json
import os

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from juniorguru.lib import loggers


MEMBERFUL_API_KEY = os.environ['MEMBERFUL_API_KEY']

MEMBERFUL_MUTATIONS_ENABLED = bool(int(os.getenv('MEMBERFUL_MUTATIONS_ENABLED', 0)))


logger = loggers.get(__name__)


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

    def query(self, query_string, get_page_info):
        cursor = ''
        query_gql = gql(query_string)
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
