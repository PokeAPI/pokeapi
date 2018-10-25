from django.test import TestCase
from graphene import Context
from graphene.test import Client
from .schema import schema
from .middleware import LoaderMiddleware
from .utils.to_plain_dict import to_plain_dict


class GraphQLTest(TestCase):
    """Base class for testing GraphQL queries."""

    maxDiff = None

    def execute_query(self, query):
        client = Client(schema)
        result = client.execute(
            query, middleware=[LoaderMiddleware()], context_value=Context()
        )

        # OrderedDicts screw up the error diffs, so convert to a normal dictionary
        return to_plain_dict(result)
